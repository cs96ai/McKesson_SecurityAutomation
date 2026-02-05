import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import PlainTextResponse, HTMLResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import httpx
from contextlib import asynccontextmanager

from simulator import WebUISimulator
from security_events import WebUISecurityEventGenerator

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(message)s'
)
logger = logging.getLogger(__name__)

APP_NAME = os.getenv("APP_NAME", "hsps-webui")
APP_TYPE = os.getenv("APP_TYPE", "webui")
SECURITY_PORTAL_URL = os.getenv("SECURITY_PORTAL_URL", "http://security-portal:8000")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default-token-change-me")
ANOMALY_FREQUENCY = float(os.getenv("ANOMALY_FREQUENCY", "0.1"))
NAMESPACE = os.getenv("NAMESPACE", "default")
POD_NAME = os.getenv("POD_NAME", "unknown-pod")
NODE_NAME = os.getenv("NODE_NAME", "unknown-node")
POD_IP = os.getenv("POD_IP", "0.0.0.0")

ui_page_views = Counter('hsps_ui_page_views_total', 'Total page views', ['page'])
ui_user_sessions = Gauge('hsps_ui_active_sessions', 'Active user sessions')
ui_form_submissions = Counter('hsps_ui_form_submissions_total', 'Form submissions', ['form_type', 'status'])
ui_xss_detections = Counter('hsps_ui_xss_detections_total', 'XSS payload detections')
ui_csrf_failures = Counter('hsps_ui_csrf_failures_total', 'CSRF token validation failures')
ui_bot_detections = Counter('hsps_ui_bot_detections_total', 'Bot-like behavior detections')
ui_file_uploads = Counter('hsps_ui_file_uploads_total', 'File upload attempts', ['file_type', 'status'])
ui_geolocation_mismatches = Counter('hsps_ui_geolocation_mismatches_total', 'Geolocation anomalies')
ui_page_load_time = Histogram('hsps_ui_page_load_seconds', 'Page load times', ['page'])
ui_clickstream_events = Counter('hsps_ui_clickstream_events_total', 'Clickstream events', ['event_type'])

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
            "/",
            "/prescriptions",
            "/medications",
            "/inventory",
            "/api/sessions",
            "/api/clickstream"
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
            
            ui_user_sessions.set(metrics['active_sessions'])
            
            for page, count in metrics['page_views'].items():
                ui_page_views.labels(page=page).inc(count)
            
            for page, load_time in metrics['page_load_times'].items():
                ui_page_load_time.labels(page=page).observe(load_time)
            
            for event_type, count in metrics['clickstream_events'].items():
                ui_clickstream_events.labels(event_type=event_type).inc(count)
            
            log_structured("INFO", "Web UI metrics generated", **metrics)
            
            if event_generator.should_generate_event():
                event = event_generator.generate_event()
                
                if event['event_type'] == 'xss_detection':
                    ui_xss_detections.inc()
                elif event['event_type'] == 'csrf_failure':
                    ui_csrf_failures.inc()
                elif event['event_type'] == 'bot_detection':
                    ui_bot_detections.inc()
                elif event['event_type'] == 'file_upload_attempt':
                    ui_file_uploads.labels(file_type=event.get('file_type', 'unknown'), status=event.get('status', 'blocked')).inc()
                elif event['event_type'] == 'geolocation_mismatch':
                    ui_geolocation_mismatches.inc()
                
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
    
    log_structured("INFO", "Starting HSPS Web UI Simulator")
    
    simulator = WebUISimulator()
    event_generator = WebUISecurityEventGenerator(anomaly_frequency=ANOMALY_FREQUENCY)
    
    await announce_to_portal()
    
    background_task = asyncio.create_task(background_simulation())
    
    yield
    
    if background_task:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass
    
    log_structured("INFO", "Shutting down HSPS Web UI Simulator")

app = FastAPI(
    title="HSPS Web UI Simulator",
    description="McKesson Health Systems Pharmacy System - Web UI Component",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    
    response = await call_next(request)
    
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    log_structured("INFO", "Web UI request processed",
                  method=request.method,
                  path=request.url.path,
                  status_code=response.status_code,
                  duration=duration,
                  client_ip=request.client.host if request.client else "unknown",
                  user_agent=request.headers.get("user-agent", "unknown"))
    
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

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HSPS - Pharmacy Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #2c3e50; }
            .nav { margin: 20px 0; }
            .nav a { margin-right: 15px; padding: 10px 15px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
            .nav a:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>McKesson Health Systems Pharmacy System</h1>
            <div class="nav">
                <a href="/prescriptions">Prescriptions</a>
                <a href="/medications">Medications</a>
                <a href="/inventory">Inventory</a>
                <a href="/orders">Orders</a>
            </div>
            <p>Welcome to the HSPS Web UI Simulator</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/prescriptions", response_class=HTMLResponse)
async def prescriptions_page():
    return HTMLResponse(content="<h1>Prescriptions Management</h1><p>Simulated page</p>")

@app.get("/medications", response_class=HTMLResponse)
async def medications_page():
    return HTMLResponse(content="<h1>Medications Database</h1><p>Simulated page</p>")

@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page():
    return HTMLResponse(content="<h1>Inventory Management</h1><p>Simulated page</p>")

@app.get("/api/sessions", dependencies=[Depends(verify_token)])
async def get_sessions():
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    sessions = simulator.get_session_stats()
    log_structured("INFO", "Session stats requested", **sessions)
    return sessions

@app.get("/api/clickstream", dependencies=[Depends(verify_token)])
async def get_clickstream():
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    clickstream = simulator.get_clickstream_data()
    log_structured("INFO", "Clickstream data requested", event_count=len(clickstream))
    return {"events": clickstream, "count": len(clickstream)}

@app.post("/api/track-event", dependencies=[Depends(verify_token)])
async def track_event(event: dict):
    if not simulator:
        raise HTTPException(status_code=503, detail="Simulator not ready")
    
    result = simulator.track_user_event(event)
    log_structured("INFO", "User event tracked", event_type=event.get('type'))
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
