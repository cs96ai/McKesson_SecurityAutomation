import os
import json
import logging
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import PlainTextResponse, HTMLResponse
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from collections import defaultdict

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format='%(message)s'
)
logger = logging.getLogger(__name__)

APP_NAME = "security-portal"
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "default-token-change-me")

registered_apps = Counter('security_portal_registered_apps_total', 'Total registered applications', ['app_type'])
security_events = Counter('security_portal_events_total', 'Total security events received', ['app_type', 'event_type', 'severity'])
active_applications = Gauge('security_portal_active_applications', 'Currently active applications', ['app_type'])

class AppRegistration(BaseModel):
    app_name: str
    app_type: str
    instance_id: str
    namespace: str
    pod_name: str
    node_name: str
    ip_address: str
    endpoints: List[str]
    version: str
    registered_at: str

class SecurityEvent(BaseModel):
    event_type: str
    severity: str
    timestamp: str

applications_registry = {}
events_storage = []

def log_structured(level: str, message: str, **kwargs):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "app_name": APP_NAME,
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

app = FastAPI(
    title="HSPS Security Portal",
    description="Central security event collector and monitoring portal",
    version="1.0.0"
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
    return {
        "status": "ready",
        "app_name": APP_NAME,
        "registered_apps": len(applications_registry),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/register", dependencies=[Depends(verify_token)])
async def register_application(registration: AppRegistration):
    applications_registry[registration.instance_id] = registration.dict()
    
    registered_apps.labels(app_type=registration.app_type).inc()
    
    app_type_count = sum(1 for app in applications_registry.values() if app['app_type'] == registration.app_type)
    active_applications.labels(app_type=registration.app_type).set(app_type_count)
    
    log_structured("INFO", "Application registered",
                  app_name=registration.app_name,
                  app_type=registration.app_type,
                  instance_id=registration.instance_id,
                  pod_name=registration.pod_name,
                  ip_address=registration.ip_address)
    
    return {
        "status": "registered",
        "instance_id": registration.instance_id,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/events", dependencies=[Depends(verify_token)])
async def receive_event(event: dict):
    event['received_at'] = datetime.utcnow().isoformat()
    events_storage.append(event)
    
    if len(events_storage) > 10000:
        events_storage.pop(0)
    
    app_type = event.get('app_type', 'unknown')
    event_type = event.get('event_type', 'unknown')
    severity = event.get('severity', 'unknown')
    
    security_events.labels(app_type=app_type, event_type=event_type, severity=severity).inc()
    
    log_structured("WARNING", "Security event received",
                  event_type=event_type,
                  severity=severity,
                  **{k: v for k, v in event.items() if k not in ['timestamp', 'received_at']})
    
    return {
        "status": "received",
        "event_id": len(events_storage),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/applications", dependencies=[Depends(verify_token)])
async def list_applications():
    return {
        "applications": list(applications_registry.values()),
        "count": len(applications_registry),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/events", dependencies=[Depends(verify_token)])
async def list_events(
    limit: int = 100,
    severity: Optional[str] = None,
    event_type: Optional[str] = None
):
    filtered_events = events_storage
    
    if severity:
        filtered_events = [e for e in filtered_events if e.get('severity') == severity]
    
    if event_type:
        filtered_events = [e for e in filtered_events if e.get('event_type') == event_type]
    
    return {
        "events": filtered_events[-limit:],
        "count": len(filtered_events),
        "total_events": len(events_storage),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/stats", dependencies=[Depends(verify_token)])
async def get_stats():
    event_counts_by_type = defaultdict(int)
    event_counts_by_severity = defaultdict(int)
    event_counts_by_app = defaultdict(int)
    
    for event in events_storage:
        event_counts_by_type[event.get('event_type', 'unknown')] += 1
        event_counts_by_severity[event.get('severity', 'unknown')] += 1
        
        for app_id, app_data in applications_registry.items():
            if event.get('pod_name', '').startswith(app_data.get('app_name', '')):
                event_counts_by_app[app_data['app_name']] += 1
                break
    
    return {
        "total_events": len(events_storage),
        "total_applications": len(applications_registry),
        "events_by_type": dict(event_counts_by_type),
        "events_by_severity": dict(event_counts_by_severity),
        "events_by_application": dict(event_counts_by_app),
        "applications_by_type": {
            "database": sum(1 for app in applications_registry.values() if app['app_type'] == 'database'),
            "api": sum(1 for app in applications_registry.values() if app['app_type'] == 'api'),
            "webui": sum(1 for app in applications_registry.values() if app['app_type'] == 'webui')
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    stats = await get_stats()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HSPS Security Portal</title>
        <meta http-equiv="refresh" content="30">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #fff; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            h1 {{ color: #4CAF50; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
            .stat-card {{ background: #2a2a2a; padding: 20px; border-radius: 8px; border-left: 4px solid #4CAF50; }}
            .stat-value {{ font-size: 2em; font-weight: bold; color: #4CAF50; }}
            .stat-label {{ color: #aaa; margin-top: 5px; }}
            .events {{ background: #2a2a2a; padding: 20px; border-radius: 8px; margin-top: 20px; }}
            .event {{ padding: 10px; margin: 10px 0; background: #333; border-radius: 4px; border-left: 3px solid #ff9800; }}
            .critical {{ border-left-color: #f44336; }}
            .high {{ border-left-color: #ff9800; }}
            .medium {{ border-left-color: #ffeb3b; }}
            .low {{ border-left-color: #4CAF50; }}
            .timestamp {{ color: #888; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ HSPS Security Portal</h1>
            <p class="timestamp">Last updated: {datetime.utcnow().isoformat()}</p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{stats['total_events']}</div>
                    <div class="stat-label">Total Security Events</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['total_applications']}</div>
                    <div class="stat-label">Registered Applications</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['applications_by_type'].get('database', 0)}</div>
                    <div class="stat-label">Database Instances</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['applications_by_type'].get('api', 0)}</div>
                    <div class="stat-label">API Instances</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{stats['applications_by_type'].get('webui', 0)}</div>
                    <div class="stat-label">Web UI Instances</div>
                </div>
            </div>
            
            <div class="events">
                <h2>Recent Security Events (Last 10)</h2>
                {''.join([f'<div class="event {event.get("severity", "").lower()}"><strong>{event.get("event_type", "Unknown")}</strong> - Severity: {event.get("severity", "Unknown")}<br><span class="timestamp">{event.get("timestamp", "")}</span></div>' for event in events_storage[-10:]][::-1]) if events_storage else '<p>No events yet</p>'}
            </div>
            
            <div class="events">
                <h2>Events by Severity</h2>
                <ul>
                    {''.join([f'<li>{severity}: {count}</li>' for severity, count in stats['events_by_severity'].items()])}
                </ul>
            </div>
            
            <div class="events">
                <h2>Events by Type</h2>
                <ul>
                    {''.join([f'<li>{event_type}: {count}</li>' for event_type, count in list(stats['events_by_type'].items())[:10]])}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
