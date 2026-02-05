import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import httpx
from contextlib import asynccontextmanager

from simulator import APISimulator
from security_events import APISecurityEventGenerator

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(message)s'
)
logger = logging.getLogger(__name__)

APP_NAME = os.getenv("APP_NAME", "hsps-api")
APP_TYPE = os.getenv("APP_TYPE", "api")
SECURITY_PORTAL_URL = os.getenv("SECURITY_PORTAL_URL", "http://security-portal:8000")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default-token-change-me")
ANOMALY_FREQUENCY = float(os.getenv("ANOMALY_FREQUENCY", "0.1"))
NAMESPACE = os.getenv("NAMESPACE", "default")
POD_NAME = os.getenv("POD_NAME", "unknown-pod")
NODE_NAME = os.getenv("NODE_NAME", "unknown-node")
POD_IP = os.getenv("POD_IP", "0.0.0.0")

api_requests = Counter('hsps_api_requests_total', 'Total API requests', ['endpoint', 'method', 'status'])
api_request_duration = Histogram('hsps_api_request_duration_seconds', 'API request duration', ['endpoint', 'method'])
api_auth_failures = Counter('hsps_api_auth_failures_total', 'API authentication failures', ['reason'])
api_rate_limit_hits = Counter('hsps_api_rate_limit_hits_total', 'Rate limit hits', ['endpoint'])
api_validation_errors = Counter('hsps_api_validation_errors_total', 'Input validation errors', ['error_type'])
api_injection_attempts = Counter('hsps_api_injection_attempts_total', 'Injection attempt detections', ['injection_type'])
api_active_sessions = Gauge('hsps_api_active_sessions', 'Active API sessions')
api_payload_size = Histogram('hsps_api_payload_size_bytes', 'API payload sizes', ['endpoint'])
api_error_rate = Gauge('hsps_api_error_rate', 'API error rate percentage')

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
        api_auth_failures.labels(reason="missing_header").inc()
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        api_auth_failures.labels(reason="invalid_format").inc()
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.replace("Bearer ", "")
    if token != BEARER_TOKEN:
        api_auth_failures.labels(reason="invalid_token").inc()
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
            "/api/v1/prescriptions",
            "/api/v1/medications",
            "/api/v1/inventory",
            "/api/v1/orders",
            "/api/v1/patients"
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
            
            api_active_sessions.set(metrics['active_sessions'])
            api_error_rate.set(metrics['error_rate'])
            
            for endpoint, count in metrics['requests_by_endpoint'].items():
                api_requests.labels(endpoint=endpoint, method='GET', status='200').inc(count)
            
            for endpoint, duration in metrics['response_times'].items():
                api_request_duration.labels(endpoint=endpoint, method='GET').observe(duration)
            
            log_structured("INFO", "API metrics generated", **metrics)
            
            if event_generator.should_generate_event():
                event = event_generator.generate_event()
                
                if event['event_type'] == 'rate_limit_exceeded':
                    api_rate_limit_hits.labels(endpoint=event['endpoint']).inc()
                elif event['event_type'] == 'validation_error':
                    api_validation_errors.labels(error_type=event['error_type']).inc()
                elif event['event_type'] in ['sql_injection', 'xss_attempt', 'command_injection']:
                    api_injection_attempts.labels(injection_type=event['event_type']).inc()
                elif event['event_type'] == 'auth_failure':
                    api_auth_failures.labels(reason=event['reason']).inc()
                
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
    
    log_structured("INFO", "Starting HSPS API Simulator")
    
    simulator = APISimulator()
    event_generator = APISecurityEventGenerator(anomaly_frequency=ANOMALY_FREQUENCY)
    
    await announce_to_portal()
    
    background_task = asyncio.create_task(background_simulation())
    
    yield
    
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    
    log_structured("INFO", "Shutting down HSPS API Simulator")

app = FastAPI(
    title="HSPS API Simulator",
    description="McKesson Health Systems Pharmacy System - API Component",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    response = await call_next(request)
    
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    log_structured("INFO", "API request processed",
                  method=request.method,
                  path=request.url.path,
                  status_code=response.status_code,
                  duration=duration,
                  client_ip=request.client.host if request.client else "unknown")
    
    return response

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

@app.get("/api/v1/prescriptions", dependencies=[Depends(verify_token)])
async def get_prescriptions(patient_id: Optional[str] = None, limit: int = 10):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    prescriptions = simulator.get_prescriptions(patient_id, limit)
    log_structured("INFO", "Prescriptions retrieved", patient_id=patient_id, count=len(prescriptions))
    return {"data": prescriptions, "count": len(prescriptions)}

@app.get("/api/v1/medications", dependencies=[Depends(verify_token)])
async def get_medications(search: Optional[str] = None, limit: int = 20):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    medications = simulator.get_medications(search, limit)
    log_structured("INFO", "Medications retrieved", search=search, count=len(medications))
    return {"data": medications, "count": len(medications)}

@app.get("/api/v1/inventory", dependencies=[Depends(verify_token)])
async def get_inventory(location: Optional[str] = None):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    inventory = simulator.get_inventory(location)
    log_structured("INFO", "Inventory retrieved", location=location, count=len(inventory))
    return {"data": inventory, "count": len(inventory)}

@app.post("/api/v1/orders", dependencies=[Depends(verify_token)])
async def create_order(order: dict):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    result = simulator.create_order(order)
    log_structured("INFO", "Order created", order_id=result['order_id'])
    return result

@app.get("/api/v1/patients/{patient_id}", dependencies=[Depends(verify_token)])
async def get_patient(patient_id: str):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    patient = simulator.get_patient(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    log_structured("INFO", "Patient retrieved", patient_id=patient_id)
    return patient

@app.get("/api/v1/stats", dependencies=[Depends(verify_token)])
async def get_api_stats():
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    stats = simulator.get_api_stats()
    return stats

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
