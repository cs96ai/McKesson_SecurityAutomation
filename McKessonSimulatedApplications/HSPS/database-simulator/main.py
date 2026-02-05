import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import httpx
from contextlib import asynccontextmanager

from simulator import DatabaseSimulator
from security_events import SecurityEventGenerator

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(message)s'
)
logger = logging.getLogger(__name__)

APP_NAME = os.getenv("APP_NAME", "hsps-database")
APP_TYPE = os.getenv("APP_TYPE", "database")
SECURITY_PORTAL_URL = os.getenv("SECURITY_PORTAL_URL", "http://security-portal:8000")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default-token-change-me")
ANOMALY_FREQUENCY = float(os.getenv("ANOMALY_FREQUENCY", "0.1"))
NAMESPACE = os.getenv("NAMESPACE", "default")
POD_NAME = os.getenv("POD_NAME", "unknown-pod")
NODE_NAME = os.getenv("NODE_NAME", "unknown-node")
POD_IP = os.getenv("POD_IP", "0.0.0.0")

db_connections = Gauge('hsps_db_connections_total', 'Total database connections')
db_queries = Counter('hsps_db_queries_total', 'Total database queries', ['query_type', 'status'])
db_query_duration = Histogram('hsps_db_query_duration_seconds', 'Database query duration', ['query_type'])
db_auth_failures = Counter('hsps_db_auth_failures_total', 'Database authentication failures', ['reason'])
db_privilege_escalations = Counter('hsps_db_privilege_escalation_attempts_total', 'Privilege escalation attempts')
db_data_exfiltration = Counter('hsps_db_data_exfiltration_bytes', 'Data exfiltration volume in bytes')
db_table_scans = Counter('hsps_db_table_scans_total', 'Full table scans', ['table_name'])
db_failed_logins = Counter('hsps_db_failed_logins_total', 'Failed login attempts', ['username'])
db_sql_injection_attempts = Counter('hsps_db_sql_injection_attempts_total', 'SQL injection attempts')
db_connection_spikes = Counter('hsps_db_connection_spikes_total', 'Connection spike events')

simulator = None
event_generator = None
background_task = None

def log_structured(level: str, message: str, **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "app_name": APP_NAME,
        "app_type": APP_TYPE,
        "pod_name": POD_NAME,
        "namespace": NAMESPACE,
        "message": message,
        **kwargs
    }
    logger.info(json.dumps(log_entry))

async def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    if token != BEARER_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    return token

async def announce_to_portal():
    announcement = {
        "app_name": APP_NAME,
        "app_type": APP_TYPE,
        "instance_id": f"{POD_NAME}-{os.getpid()}",
        "namespace": NAMESPACE,
        "pod_name": POD_NAME,
        "node_name": NODE_NAME,
        "ip_address": POD_IP,
        "endpoints": [
            "/health",
            "/ready",
            "/metrics",
            "/api/connections",
            "/api/queries"
        ],
        "version": "1.0.0",
        "registered_at": datetime.utcnow().isoformat()
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{SECURITY_PORTAL_URL}/api/register",
                json=announcement,
                headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
            )
            if response.status_code == 200:
                log_structured("INFO", "Successfully registered with security portal", **announcement)
            else:
                log_structured("WARNING", "Failed to register with security portal", 
                             status_code=response.status_code, response=response.text)
    except Exception as e:
        log_structured("ERROR", "Error announcing to security portal", error=str(e))

async def background_simulation():
    global simulator, event_generator
    
    while True:
        try:
            metrics = simulator.generate_metrics()
            
            db_connections.set(metrics['active_connections'])
            
            for query_type, count in metrics['queries_by_type'].items():
                db_queries.labels(query_type=query_type, status='success').inc(count)
            
            for query_type, duration in metrics['query_durations'].items():
                db_query_duration.labels(query_type=query_type).observe(duration)
            
            log_structured("INFO", "Database metrics generated", **metrics)
            
            if event_generator.should_generate_event():
                event = event_generator.generate_event()
                
                if event['event_type'] == 'auth_failure':
                    db_auth_failures.labels(reason=event['reason']).inc()
                elif event['event_type'] == 'privilege_escalation':
                    db_privilege_escalations.inc()
                elif event['event_type'] == 'data_exfiltration':
                    db_data_exfiltration.inc(event['bytes_transferred'])
                elif event['event_type'] == 'sql_injection':
                    db_sql_injection_attempts.inc()
                elif event['event_type'] == 'connection_spike':
                    db_connection_spikes.inc()
                elif event['event_type'] == 'failed_login':
                    db_failed_logins.labels(username=event['username']).inc()
                
                log_structured("WARNING", "Security event detected", **event)
                
                try:
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        await client.post(
                            f"{SECURITY_PORTAL_URL}/api/events",
                            json=event,
                            headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
                        )
                except Exception as e:
                    log_structured("ERROR", "Failed to send event to portal", error=str(e))
            
            await asyncio.sleep(5)
            
        except Exception as e:
            log_structured("ERROR", "Error in background simulation", error=str(e))
            await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global simulator, event_generator, background_task
    
    log_structured("INFO", "Starting HSPS Database Simulator")
    
    simulator = DatabaseSimulator()
    event_generator = SecurityEventGenerator(anomaly_frequency=ANOMALY_FREQUENCY)
    
    await announce_to_portal()
    
    background_task = asyncio.create_task(background_simulation())
    
    yield
    
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    
    log_structured("INFO", "Shutting down HSPS Database Simulator")

app = FastAPI(
    title="HSPS Database Simulator",
    description="McKesson Health Systems Pharmacy System - Database Component",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": APP_NAME,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    if simulator is None:
        raise HTTPException(status_code=503, detail="Simulator not initialized")
    
    return {
        "status": "ready",
        "app_name": APP_NAME,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/connections", dependencies=[Depends(verify_token)])
async def get_connections():
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    connections = simulator.get_connection_stats()
    log_structured("INFO", "Connection stats requested", **connections)
    return connections

@app.get("/api/queries", dependencies=[Depends(verify_token)])
async def get_queries():
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    queries = simulator.get_query_stats()
    log_structured("INFO", "Query stats requested", **queries)
    return queries

@app.post("/api/execute-query", dependencies=[Depends(verify_token)])
async def execute_query(query: dict):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    result = simulator.execute_simulated_query(query.get("sql", ""))
    
    log_structured("INFO", "Query executed", 
                  query=query.get("sql", "")[:100],
                  duration=result['duration'],
                  rows_affected=result['rows_affected'])
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
