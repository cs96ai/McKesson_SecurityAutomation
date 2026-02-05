# McKesson HSPS - Cybersecurity Monitoring Demo

A comprehensive Kubernetes-based cybersecurity monitoring demonstration for the McKesson Health Systems Pharmacy System (HSPS) with simulated applications that emit security-relevant telemetry data.

## Overview

This demo environment includes 3 simulated applications plus a central security portal:

1. **Database Simulator** - PostgreSQL-like database with security telemetry
2. **API Simulator** - RESTful service with security events
3. **Web UI Simulator** - Frontend application with user behavior telemetry
4. **Security Portal** - Central collector and monitoring dashboard

All applications emit structured logs, Prometheus metrics, and security events that demonstrate real-world cybersecurity monitoring scenarios.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster (hsps namespace)       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Database   │  │     API      │  │    Web UI    │      │
│  │  Simulator   │  │  Simulator   │  │  Simulator   │      │
│  │  (2 pods)    │  │  (3 pods)    │  │  (2 pods)    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           │                                  │
│                  ┌────────▼────────┐                         │
│                  │  Security Portal│                         │
│                  │    (1 pod)      │                         │
│                  └────────┬────────┘                         │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐               │
│         │                 │                 │               │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌─────▼──────┐        │
│  │  Prometheus  │  │   Grafana    │  │   Logs     │        │
│  │  (Metrics)   │  │ (Dashboard)  │  │  (stdout)  │        │
│  └──────────────┘  └──────────────┘  └────────────┘        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Features

### Database Simulator
Emits security telemetry for:
- Connection attempts (success/failed)
- Query execution times
- Authentication failures
- Privilege escalation attempts
- Data exfiltration patterns
- SQL injection attempts
- Failed login attempts
- Connection spikes

### API Simulator
Emits security events for:
- Request rates per endpoint
- Authentication/authorization failures
- Input validation errors
- Rate limiting events
- SQL/XSS/Command injection attempts
- API key abuse
- DDoS attempts
- Payload size violations

### Web UI Simulator
Emits user behavior telemetry for:
- User session metrics
- Clickstream data
- Form submission patterns
- XSS payload detection
- CSRF token validation failures
- Bot-like behavior patterns
- Geolocation mismatches
- File upload attempts
- Session hijacking

### Security Portal
Central collector that:
- Receives application registrations
- Collects security events
- Provides web dashboard
- Exposes Prometheus metrics
- Stores event history
- Displays real-time statistics

## Prerequisites

- Docker Desktop with Kubernetes enabled OR
- Kubernetes cluster (minikube, kind, etc.)
- kubectl configured
- Docker CLI

## Quick Start

### Option 1: Docker Compose (Local Testing)

```bash
# Navigate to the HSPS directory
cd McKessonApplications/HSPS

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access services:
# - Security Portal: http://localhost:8000
# - Database Simulator: http://localhost:8001
# - API Simulator: http://localhost:8002
# - Web UI Simulator: http://localhost:8003
# - Prometheus: http://localhost:9090
# - Grafana: http://localhost:3000 (admin/admin)

# Stop all services
docker-compose down
```

### Option 2: Kubernetes Deployment

#### Windows (PowerShell)

```powershell
cd McKessonApplications\HSPS
.\deploy-all.ps1
```

#### Linux/Mac (Bash)

```bash
cd McKessonApplications/HSPS
chmod +x deploy-all.sh
./deploy-all.sh
```

## Accessing the Applications

### Security Portal Dashboard

```bash
kubectl port-forward -n hsps svc/security-portal 8000:8000
```
Visit: http://localhost:8000

The dashboard shows:
- Total security events
- Registered applications
- Recent security events
- Events by severity and type

### Prometheus

```bash
kubectl port-forward -n hsps svc/prometheus 9090:9090
```
Visit: http://localhost:9090

### Grafana

```bash
kubectl port-forward -n hsps svc/grafana 3000:3000
```
Visit: http://localhost:3000
- Username: `admin`
- Password: `admin`

## Viewing Logs

### All applications

```bash
kubectl logs -f -n hsps --all-containers=true
```

### Specific application

```bash
# Security Portal
kubectl logs -f -n hsps -l app=security-portal

# Database Simulator
kubectl logs -f -n hsps -l app=hsps-database-simulator

# API Simulator
kubectl logs -f -n hsps -l app=hsps-api-simulator

# Web UI Simulator
kubectl logs -f -n hsps -l app=hsps-webui-simulator
```

## API Endpoints

### Security Portal

- `GET /` - Web dashboard
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Prometheus metrics
- `POST /api/register` - Application registration (requires Bearer token)
- `POST /api/events` - Receive security events (requires Bearer token)
- `GET /api/applications` - List registered applications (requires Bearer token)
- `GET /api/events` - List security events (requires Bearer token)
- `GET /api/stats` - Get statistics (requires Bearer token)

### Database Simulator

- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Prometheus metrics
- `GET /api/connections` - Connection statistics (requires Bearer token)
- `GET /api/queries` - Query statistics (requires Bearer token)
- `POST /api/execute-query` - Execute simulated query (requires Bearer token)

### API Simulator

- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Prometheus metrics
- `GET /api/v1/prescriptions` - Get prescriptions (requires Bearer token)
- `GET /api/v1/medications` - Get medications (requires Bearer token)
- `GET /api/v1/inventory` - Get inventory (requires Bearer token)
- `POST /api/v1/orders` - Create order (requires Bearer token)
- `GET /api/v1/patients/{id}` - Get patient (requires Bearer token)
- `GET /api/v1/stats` - API statistics (requires Bearer token)

### Web UI Simulator

- `GET /` - Home page
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Prometheus metrics
- `GET /prescriptions` - Prescriptions page
- `GET /medications` - Medications page
- `GET /inventory` - Inventory page
- `GET /api/sessions` - Session statistics (requires Bearer token)
- `GET /api/clickstream` - Clickstream data (requires Bearer token)
- `POST /api/track-event` - Track user event (requires Bearer token)

## Security Events Generated

The simulators randomly generate these security events (configurable via `ANOMALY_FREQUENCY`):

### Database Events
- Authentication failures
- Privilege escalation attempts
- Data exfiltration
- SQL injection attempts
- Connection spikes
- Failed logins
- Unusual query patterns
- Brute force attacks

### API Events
- Rate limit exceeded
- Authentication failures
- Validation errors
- SQL injection
- XSS attempts
- Command injection
- API key abuse
- Unusual access patterns
- Payload size exceeded
- DDoS attempts

### Web UI Events
- XSS detection
- CSRF failures
- Bot detection
- File upload attempts
- Geolocation mismatches
- Session hijacking
- Clickjacking attempts
- Form tampering
- Suspicious navigation

## Configuration

### Environment Variables

All applications support these environment variables:

- `APP_NAME` - Application identifier
- `APP_TYPE` - Application type (database/api/webui)
- `SECURITY_PORTAL_URL` - Security portal URL
- `BEARER_TOKEN` - Authentication token
- `ANOMALY_FREQUENCY` - Frequency of anomaly generation (0.0-1.0, default: 0.1)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)

### Kubernetes ConfigMap

Edit `database-simulator/kubernetes/configmap.yaml`:

```yaml
data:
  security_portal_url: "http://security-portal:8000"
  anomaly_frequency: "0.15"  # 15% chance of generating anomaly every 5 seconds
  log_level: "INFO"
```

### Kubernetes Secret

Edit `database-simulator/kubernetes/secret.yaml`:

```yaml
stringData:
  bearer_token: "your-secure-token-here"
```

## Prometheus Metrics

### Database Simulator Metrics
- `hsps_db_connections_total` - Total database connections
- `hsps_db_queries_total` - Total queries by type and status
- `hsps_db_query_duration_seconds` - Query duration histogram
- `hsps_db_auth_failures_total` - Authentication failures
- `hsps_db_privilege_escalation_attempts_total` - Privilege escalation attempts
- `hsps_db_sql_injection_attempts_total` - SQL injection attempts

### API Simulator Metrics
- `hsps_api_requests_total` - Total API requests
- `hsps_api_request_duration_seconds` - Request duration histogram
- `hsps_api_auth_failures_total` - Authentication failures
- `hsps_api_rate_limit_hits_total` - Rate limit hits
- `hsps_api_injection_attempts_total` - Injection attempts
- `hsps_api_active_sessions` - Active API sessions

### Web UI Simulator Metrics
- `hsps_ui_page_views_total` - Total page views
- `hsps_ui_active_sessions` - Active user sessions
- `hsps_ui_xss_detections_total` - XSS detections
- `hsps_ui_csrf_failures_total` - CSRF failures
- `hsps_ui_bot_detections_total` - Bot detections
- `hsps_ui_file_uploads_total` - File upload attempts

### Security Portal Metrics
- `security_portal_registered_apps_total` - Registered applications
- `security_portal_events_total` - Security events received
- `security_portal_active_applications` - Active applications

## Example Queries

### Prometheus Queries

```promql
# Total security events by type
sum by (event_type) (security_portal_events_total)

# Database authentication failure rate
rate(hsps_db_auth_failures_total[5m])

# API request rate
rate(hsps_api_requests_total[1m])

# Web UI XSS detection rate
rate(hsps_ui_xss_detections_total[5m])

# P95 query latency
histogram_quantile(0.95, rate(hsps_db_query_duration_seconds_bucket[5m]))
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -n hsps

# Describe pod for events
kubectl describe pod <pod-name> -n hsps

# Check logs
kubectl logs <pod-name> -n hsps
```

### Applications not registering

```bash
# Check security portal logs
kubectl logs -f -n hsps -l app=security-portal

# Verify network connectivity
kubectl exec -it <pod-name> -n hsps -- curl http://security-portal:8000/health
```

### No metrics in Prometheus

```bash
# Check Prometheus targets
kubectl port-forward -n hsps svc/prometheus 9090:9090
# Visit http://localhost:9090/targets

# Verify metrics endpoint
kubectl exec -it <pod-name> -n hsps -- curl http://localhost:8000/metrics
```

## Cleanup

### Docker Compose

```bash
docker-compose down -v
```

### Kubernetes

```bash
kubectl delete namespace hsps
```

## Project Structure

```
HSPS/
├── database-simulator/
│   ├── main.py
│   ├── simulator.py
│   ├── security_events.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       ├── secret.yaml
│       └── serviceaccount.yaml
├── api-simulator/
│   ├── main.py
│   ├── simulator.py
│   ├── security_events.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── serviceaccount.yaml
├── webui-simulator/
│   ├── main.py
│   ├── simulator.py
│   ├── security_events.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── serviceaccount.yaml
├── security-portal/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── kubernetes/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── serviceaccount.yaml
├── kubernetes/
│   └── namespace.yaml
├── monitoring/
│   ├── prometheus-config.yaml
│   ├── prometheus-local.yml
│   └── grafana-config.yaml
├── docker-compose.yml
├── deploy-all.sh
├── deploy-all.ps1
└── README.md
```

## License

This is a demonstration project for educational and testing purposes.

## Support

For issues or questions, please refer to the project documentation or contact the development team.
