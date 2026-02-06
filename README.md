# McKesson Security Automation Platform

A proof-of-concept security operations platform built to demonstrate end-to-end security automation across Azure, Kubernetes, and AI-assisted operations. The platform simulates two healthcare systems (HSPS and STAR), monitors them for security events in real time, and provides playbook-driven incident response through a modern Vue 3 SPA.

> **Live Demo**: [mckessondemo-csutherland.azurewebsites.net](https://mckessondemo-csutherland.azurewebsites.net)

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Vue 3 SPA (Azure App Service)                │
│  Dashboard · Playbooks · ChatOps · Kubernetes Monitor · CI/CD · ...  │
└────────────────────────────┬─────────────────────────────────────────┘
                             │  REST / Bearer Token
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Azure App Service)                 │
│           14 read-only Azure endpoints · OpenAI ChatOps agent        │
│         Read-only service principal · Kubernetes API access          │
└────────────┬──────────────────────────────────┬──────────────────────┘
             │                                  │
             ▼                                  ▼
┌────────────────────────────┐   ┌─────────────────────────────────────┐
│     OpenAI GPT-4 API       │   │      Azure Kubernetes Service       │
│  Natural language queries  │   │                                     │
│  with security guardrails  │   │  ┌─────────────┐ ┌─────────────┐   │
└────────────────────────────┘   │  │    HSPS     │ │    STAR     │   │
                                 │  │  Namespace  │ │  Namespace  │   │
                                 │  ├─────────────┤ ├─────────────┤   │
                                 │  │ Database    │ │ Database    │   │
                                 │  │ API         │ │ API         │   │
                                 │  │ Web UI      │ │ Web UI      │   │
                                 │  │ Sec Portal  │ │ Sec Portal  │   │
                                 │  └─────────────┘ └─────────────┘   │
                                 └──────────────┬──────────────────────┘
                                                │
                                                ▼
                                 ┌─────────────────────────────────────┐
                                 │  Azure Function (Timer Trigger)     │
                                 │  Pod auto-shutdown every 5 min      │
                                 │  Managed Identity auth to AKS       │
                                 └─────────────────────────────────────┘
```

---

## What This Demonstrates

| Skill Area | Implementation |
|---|---|
| **Security Orchestration** | 12 automated playbooks (endpoint remediation, phishing response, SIEM enrichment, DLP, malware analysis, etc.) with execution tracking and success metrics |
| **Kubernetes Security Monitoring** | Python simulators running in AKS that emit realistic security events (SQLi, XSS, privilege escalation, PHI exfiltration, prescription fraud) collected by a central Security Portal |
| **AI-Assisted SecOps (ChatOps)** | GPT-4 integration with 4-layer security: client-side pattern detection, system prompt guardrails, backend auth, and Azure RBAC (Reader role). Violation counter auto-resets the session after 3 attempts |
| **Azure Infrastructure** | AKS cluster, App Services, Azure Functions, Container Registry, managed identities, read-only service principals |
| **Backend API Design** | FastAPI with 14 read-only Azure endpoints, bearer token auth, Kubernetes API access via AKS credential retrieval |
| **Infrastructure Automation** | PowerShell deployment scripts, Azure Function timer triggers for pod lifecycle management, Docker containerization |
| **Frontend Engineering** | Vue 3 + Composition API, Pinia state management, TailwindCSS, real-time event streaming, dark mode |

---

## Key Components

### Security Automation UI (`McKesson_SecurityAutomation_UI/`)

Vue 3 single-page application with 9 views:

- **Dashboard** -- KPIs, toil reduction metrics, quarterly objectives, automation roadmap
- **Playbooks** -- 12 security playbooks with execution history, success rates, and simulated runs
- **Self-Service** -- CLI simulator, ChatOps AI interface, quick actions (triage, isolate, scan)
- **Kubernetes Monitor** -- Live event stream from HSPS/STAR pods with auto-refresh, pod health, and resource metrics
- **Integrations** -- 15 security tool connections (Splunk, CrowdStrike, ServiceNow, SentinelOne, etc.)
- **CI/CD** -- Pipeline management, deployment tracking, secrets rotation
- **Observability** -- Metrics, distributed tracing, alerting, error budgets
- **Collaboration** -- Team coordination and knowledge base
- **Settings** -- User profile, preferences, dark mode

### Backend API (`McKesson_SecurityAutomation_API/`)

Python FastAPI server providing:

- **14 read-only Azure endpoints** -- AKS status, pod listing, deployments, services, logs, resource groups, app services, node pools, subscription info
- **OpenAI agent endpoint** -- `/api/agent/chat` for natural language infrastructure queries
- **Authentication** -- Bearer token verification on all endpoints
- **Azure SDK integration** -- `azure-identity`, `azure-mgmt-resource`, `azure-mgmt-containerservice`, `kubernetes` client

### Simulated Healthcare Systems (`McKessonSimulatedApplications/`)

Two Dockerized systems deployed to AKS, each with 4 microservices:

**HSPS (Healthcare Provider System)** -- Generates security events: auth failures, SQL injection, privilege escalation, data exfiltration, brute force attacks

**STAR (Pharmacy System)** -- Generates healthcare-specific events: prescription fraud, DEA verification failures, controlled substance access, insurance claim manipulation, PHI violations

Each system includes:
- Database simulator (connection monitoring, query analysis)
- API simulator (request rate tracking, injection detection)
- Web UI simulator (session tracking, XSS/CSRF/bot detection)
- Security Portal (event aggregation, Prometheus metrics, web dashboard)

### ChatOps Security Model

```
┌──────────────────────────────────────────────────────┐
│  Layer 1: Client-Side Pattern Detection              │
│  Regex matching for destructive commands & creds     │
│  Hidden violation counter (max 3, then auto-reset)   │
├──────────────────────────────────────────────────────┤
│  Layer 2: OpenAI System Prompt Guardrails            │
│  Strict read-only instructions in system message     │
│  Forbidden action categories in prompt engineering   │
├──────────────────────────────────────────────────────┤
│  Layer 3: Backend API Authentication                 │
│  Bearer token required on every request              │
│  Server-side Azure calls (no creds in browser)       │
├──────────────────────────────────────────────────────┤
│  Layer 4: Azure RBAC (Reader Role)                   │
│  Service principal physically cannot write/delete    │
│  Enforced at the Azure platform level                │
└──────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Vue 3, Vite, TailwindCSS, Pinia, Vue Router, Chart.js |
| **Backend API** | Python, FastAPI, Uvicorn, Azure SDK, Kubernetes client |
| **Simulators** | Python, FastAPI, Prometheus client, Docker |
| **Infrastructure** | Azure App Service, AKS, Azure Functions, Azure Container Registry |
| **AI** | OpenAI GPT-4 API |
| **Automation** | PowerShell, Azure CLI, kubectl |

---

## Project Structure

```
McKesson_DevSecAutomation/
├── McKesson_SecurityAutomation_UI/       # Vue 3 SPA
│   └── src/
│       ├── views/                        # 9 page components
│       ├── stores/                       # Pinia state (6 stores)
│       ├── services/                     # Azure API + OpenAI clients
│       └── config/                       # Environment management
│
├── McKesson_SecurityAutomation_API/      # FastAPI backend
│   ├── main.py                           # 14 Azure endpoints + agent
│   └── requirements.txt
│
├── McKessonSimulatedApplications/
│   ├── HSPS/                             # Healthcare Provider System
│   │   ├── database-simulator/           # Python + Docker
│   │   ├── api-simulator/               # Python + Docker
│   │   ├── webui-simulator/             # Python + Docker
│   │   ├── security-portal/             # Event aggregator
│   │   └── kubernetes/                  # K8s manifests
│   └── STAR/                             # Pharmacy System (same structure)
│
├── azure-function-pod-shutdown/          # Timer-triggered auto-shutdown
│   └── PodShutdownTimer/
│       ├── function.json                 # Cron: every 5 min
│       └── run.ps1                       # Pod age check + scale-down
│
└── auto-shutdown-pods.ps1                # Manual shutdown script
```

---

## Running Locally

**Prerequisites**: Azure CLI, kubectl, Node.js 18+, Python 3.11+, PowerShell 7+

```bash
# Frontend
cd McKesson_SecurityAutomation_UI
npm install && npm run dev            # http://localhost:5173

# Backend API
cd McKesson_SecurityAutomation_API
pip install -r requirements.txt
python -m uvicorn main:app --port 8000

# View simulated security events (requires AKS + port-forward)
kubectl port-forward -n hsps svc/security-portal 8000:8000
```

---

## Additional Documentation

- [ChatOps Security Setup](CHATOPS-SECURITY-SETUP.md) -- Security layers, violation detection, and Azure service principal configuration
- [ChatOps Azure Capabilities](CHATOPS-AZURE-CAPABILITIES.md) -- All 14 read-only Azure endpoints with query examples
- [Azure Function Setup](AZURE-FUNCTION-SETUP-COMPLETE.md) -- Timer trigger deployment and managed identity configuration
- [Auto-Shutdown](AUTO-SHUTDOWN-README.md) -- Pod lifecycle management details
