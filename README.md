# McKesson Security Automation Platform

> **⚠️ DEMO APPLICATION**: This is a demonstration platform showcasing security automation concepts and Azure/Kubernetes integration. See [Production Considerations](#-production-considerations) for required improvements before production use.

A comprehensive security automation platform demonstrating enterprise-grade security orchestration, automated response capabilities, and real-time monitoring for healthcare applications running on Azure Kubernetes Service (AKS).

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Components](#-components)
- [Getting Started](#-getting-started)
- [Deployment](#-deployment)
- [Cost Optimization](#-cost-optimization)
- [Production Considerations](#-production-considerations)
- [License](#-license)

---

## 🎯 Overview

The McKesson Security Automation Platform is a modern web-based security operations center (SOC) that demonstrates:

- **Automated Security Playbooks**: Pre-built workflows for common security incidents
- **Real-time Kubernetes Monitoring**: Live event streaming from containerized applications
- **Self-Service Security Tools**: Empowering teams with automated security tasks
- **Integration Framework**: Connecting with SIEM, EDR, and other security tools
- **CI/CD Security Integration**: Embedding security into the development pipeline
- **Cost-Aware Auto-Shutdown**: Azure Functions-based pod lifecycle management

### Use Cases

This platform demonstrates how to:
- Automate incident response for healthcare applications (HSPS & STAR pharmacy systems)
- Monitor security events across multiple Kubernetes namespaces in real-time
- Implement security-as-code with automated playbooks
- Reduce cloud costs through intelligent resource management
- Provide self-service security capabilities to development teams

---

## ✨ Features

### 1. **Security Playbooks** 🛡️

Automated security workflows for common scenarios:

- **Endpoint Remediation**: Isolate compromised endpoints and collect forensics
- **SIEM Alert Enrichment**: Automatically enrich security alerts with context
- **Phishing Response**: Automated email analysis and user notification
- **Vulnerability Patching**: Coordinate patch deployment across systems
- **Access Review**: Automated privilege access reviews
- **Compliance Reporting**: Generate compliance reports on-demand
- **Threat Intelligence**: Integrate external threat feeds
- **Incident Escalation**: Automated escalation workflows
- **Data Loss Prevention**: Detect and prevent sensitive data exfiltration
- **Malware Analysis**: Automated malware sandbox analysis
- **User Behavior Analytics**: Detect anomalous user behavior
- **Security Audit**: Comprehensive security posture assessment

**Features**:
- Execution history tracking
- Success rate monitoring
- Manual and automated triggers
- Simulated execution with realistic output
- Average execution time metrics

### 2. **Kubernetes Live Monitoring** 📊

Real-time security event monitoring for containerized applications:

- **Multi-Application Support**: Monitor HSPS and STAR healthcare systems simultaneously
- **Live Event Streaming**: Real-time security events from all pods
- **Application Filtering**: View events for all apps or filter by specific application
- **System Badges**: Visual distinction between HSPS and STAR systems
- **Event Categorization**: Security events categorized by type and severity
- **Pod Status Tracking**: Real-time pod health and restart monitoring
- **Resource Metrics**: CPU, memory, and network usage per application
- **Beautiful Loading Animation**: 7-step initialization process showing:
  - Azure connection
  - AKS authentication
  - Pod status checks
  - Application startup (HSPS & STAR)
  - Event stream establishment
  - Live data retrieval

**Event Types Monitored**:
- Authentication failures
- SQL injection attempts
- Privilege escalation
- Data exfiltration
- API abuse
- XSS/CSRF attacks
- Bot detection
- Prescription fraud (STAR-specific)
- PHI access violations (healthcare-specific)

### 3. **Self-Service Portal** �

Empower teams with automated security tools:

- **Credential Rotation**: Automated password and API key rotation
- **Certificate Management**: SSL/TLS certificate lifecycle management
- **Security Scanning**: On-demand vulnerability and compliance scans
- **Access Requests**: Streamlined temporary access provisioning

### 3.1 **AI-Powered ChatOps (OpenAI Integration)** 🤖

**EXTREME SECURITY MODE** - Read-only AI assistant with multiple security layers:

- **OpenAI GPT-4 Integration**: Natural language queries about system status
- **15 Read-Only Azure Capabilities**: Retrieves REAL data from Azure APIs
- **Backend API Service**: All Azure calls happen server-side (Node.js/Express)
- **Strict Read-Only Enforcement**: AI cannot modify, delete, or scale infrastructure
- **Security Violation Detection**: Monitors and blocks unauthorized requests
- **Hidden Violation Counter**: Tracks attempts to bypass security (max 3)
- **Auto-Reset Protection**: "Sorry Dave, I can't do that..." - resets after 3 violations
- **Azure Read-Only Access**: Service principal with Reader role only
- **Zero Credential Exposure**: Never provides API keys, secrets, or sensitive data

**15 Azure Capabilities**:
1. Get AKS Cluster Status
2. List HSPS Pods
3. List STAR Pods
4. Get Pod Details
5. Get Resource Group Info
6. List All Resources
7. Get App Service Status
8. Get Function App Status
9. Get Storage Account Info
10. Get AKS Node Pools
11. Get Deployment Status
12. Get Service Status
13. Get Pod Logs
14. Get Subscription Info
15. Get Cost Analysis

**Security Layers**:
1. Client-side pattern detection (destructive commands, credential requests)
2. OpenAI system prompt guardrails (read-only instructions)
3. Backend API authentication (Bearer token)
4. Azure RBAC (Reader role - physical access control)

See [CHATOPS-SECURITY-SETUP.md](CHATOPS-SECURITY-SETUP.md) for security configuration.
See [CHATOPS-AZURE-CAPABILITIES.md](CHATOPS-AZURE-CAPABILITIES.md) for all 15 capabilities.

- **Log Analysis**: Automated log parsing and threat detection
- **Backup Verification**: Automated backup integrity checks

### 4. **Integration Hub** 🔌

Connect with enterprise security tools:

- **SIEM Integration**: Splunk, QRadar, Sentinel
- **EDR Platforms**: CrowdStrike, Carbon Black, SentinelOne
- **Ticketing Systems**: ServiceNow, Jira, PagerDuty
- **Cloud Providers**: Azure, AWS, GCP
- **Identity Providers**: Azure AD, Okta, Auth0
- **Communication**: Slack, Teams, Email

### 5. **CI/CD Security** 🚀

Security embedded in the development pipeline:

- **Pipeline Monitoring**: Real-time build and deployment tracking
- **Security Gate Integration**: Automated security checks in CI/CD
- **Vulnerability Scanning**: Container and dependency scanning
- **Compliance Validation**: Policy enforcement before deployment
- **Deployment History**: Audit trail of all deployments

### 6. **Observability Dashboard** 📈

Comprehensive security metrics and monitoring:

- **Security Metrics**: Real-time security KPIs
- **Trend Analysis**: Historical security event trends
- **Alerting**: Configurable alerts for security events
- **Custom Dashboards**: Tailored views for different teams
- **Export Capabilities**: Data export for reporting

### 7. **Cost Optimization** 💰

**Azure Functions Auto-Shutdown**:
- Automatically shuts down Kubernetes pods after 15 minutes of runtime
- Runs every 5 minutes via Timer Trigger
- Monitors HSPS and STAR namespaces
- **Cost Savings**: ~$140-190/month
- **Function Cost**: $0/month (within free tier)
- Managed identity for secure AKS access
- Detailed execution logging

---

## 🏗️ Architecture

### Technology Stack

**Frontend**:
- Vue 3 (Composition API)
- Vite (Build tool)
- TailwindCSS (Styling)
- Pinia (State management)
- Vue Router (Navigation)
- Vue Toastification (Notifications)

**Backend/Infrastructure**:
- Azure Kubernetes Service (AKS)
- Azure Functions (PowerShell 7.4)
- Azure Static Web Apps
- Azure Container Registry
- Python FastAPI (Security Portal API)
- Docker (Containerization)

**DevOps**:
- PowerShell (Automation scripts)
- Azure CLI
- kubectl
- Git/GitHub

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure App Service                         │
│                  (McKessonDemo Vue SPA)                      │
│        https://mckessondemo-csutherland.azurewebsites.net    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Azure Kubernetes Service (AKS)                  │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │  HSPS Namespace  │        │  STAR Namespace  │          │
│  ├──────────────────┤        ├──────────────────┤          │
│  │ • Database       │        │ • Database       │          │
│  │ • API            │        │ • API            │          │
│  │ • Web UI         │        │ • Web UI         │          │
│  │ • Security Portal│        │ • Security Portal│          │
│  └──────────────────┘        └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Azure Functions (Consumption)                   │
│                  PodShutdownTimer                            │
│              (Runs every 5 minutes)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Components

### 1. **McKessonDemo Vue SPA** (`McKesson_SecurityAutomation_UI/`)

Modern single-page application with:
- Dark mode by default
- Responsive design
- Real-time data updates
- Beautiful loading animations
- Toast notifications
- Intuitive navigation

**Pages**:
- Dashboard: Overview of security posture
- Playbooks: Security automation workflows
- Self-Service: Automated security tools
- Integrations: Third-party tool connections
- CI/CD: Pipeline security monitoring
- Observability: Metrics and dashboards
- Kubernetes: Live pod monitoring
- Collaboration: Team coordination
- Settings: User preferences

### 2. **HSPS Healthcare System** (`McKessonSimulatedApplications/HSPS/`)

Simulated healthcare provider system with:
- Database simulator (PostgreSQL-like)
- API simulator (REST endpoints)
- Web UI simulator (Patient portal)
- Security Portal (Event aggregation)

**Security Events**:
- Authentication failures
- SQL injection attempts
- Privilege escalation
- Data exfiltration attempts

### 3. **STAR Pharmacy System** (`McKessonSimulatedApplications/STAR/`)

Simulated pharmacy management system with:
- Database simulator (Prescription data)
- API simulator (Pharmacy operations)
- Web UI simulator (Pharmacist interface)
- Security Portal (Compliance monitoring)

**Security Events**:
- Prescription fraud attempts
- DEA verification failures
- Controlled substance access
- PHI exfiltration attempts
- Insurance claim manipulation

### 4. **Azure Function Auto-Shutdown** (`azure-function-pod-shutdown/`)

PowerShell-based serverless function:
- Timer Trigger (every 5 minutes)
- Managed Identity authentication
- Pod age calculation
- Automatic deployment scaling
- Comprehensive logging

---

## 🚀 Getting Started

### Prerequisites

- Azure subscription
- Azure CLI installed
- kubectl installed
- Node.js 18+ and npm
- PowerShell 7+
- Git

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cs96ai/McKesson_SecurityAutomation.git
   cd McKesson_SecurityAutomation
   ```

2. **Deploy HSPS to AKS**:
   ```powershell
   cd McKessonSimulatedApplications/HSPS
   .\deploy-hsps-to-aks.ps1
   ```

3. **Deploy STAR to AKS**:
   ```powershell
   cd ../STAR
   .\deploy-star-to-aks.ps1
   ```

4. **Build and deploy Vue SPA**:
   ```powershell
   cd ../../McKesson_SecurityAutomation_UI
   npm install
   npm run build
   az webapp deploy --resource-group hsps-demo-rg --name mckessondemo-csutherland --src-path vue-app-deployment.zip --type zip
   ```

5. **Deploy Auto-Shutdown Function**:
   ```powershell
   cd ../azure-function-pod-shutdown
   # Function already deployed to hsps-pod-shutdown
   # See AZURE-FUNCTION-SETUP-COMPLETE.md for details
   ```

---

## 📚 Deployment

### Azure Resources Created

- **Resource Group**: `hsps-demo-rg`
- **AKS Cluster**: `hsps-aks-cluster`
- **Container Registry**: `hspsdemo6478`
- **App Service**: `mckessondemo-csutherland`
- **Function App**: `hsps-pod-shutdown`
- **Storage Account**: `hspspodshutdown`

### Deployment Scripts

- `McKessonSimulatedApplications/HSPS/deploy-hsps-to-aks.ps1` - Deploy HSPS system
- `McKessonSimulatedApplications/STAR/deploy-star-to-aks.ps1` - Deploy STAR system
- `auto-shutdown-pods.ps1` - Manual pod shutdown script
- `azure-function-pod-shutdown/` - Automated shutdown function

### Monitoring

**View Function Logs**:
```powershell
az functionapp log tail --resource-group hsps-demo-rg --name hsps-pod-shutdown
```

**Check Pod Status**:
```powershell
kubectl get pods -n hsps
kubectl get pods -n star
```

**View Security Events**:
```powershell
kubectl port-forward -n hsps svc/security-portal 8000:8000
# Access: http://localhost:8000/api/events
```

---

## 💰 Cost Optimization

### Auto-Shutdown System

The platform includes an Azure Functions-based auto-shutdown system that:

- **Monitors**: All pods in HSPS and STAR namespaces
- **Checks**: Pod age every 5 minutes
- **Shuts Down**: Pods running longer than 15 minutes
- **Saves**: ~$140-190/month in compute costs
- **Costs**: $0/month (within Azure Functions free tier)

**Monthly Cost Breakdown**:
- Without auto-shutdown: ~$150-200/month
- With auto-shutdown: ~$5-10/month
- **Net Savings**: ~$140-190/month (95% reduction)

### Manual Shutdown

```powershell
# Stop all HSPS pods
kubectl scale deployment --all -n hsps --replicas=0

# Stop all STAR pods
kubectl scale deployment --all -n star --replicas=0
```

---

## ⚠️ Production Considerations

### 🔴 CRITICAL: This is a Demo Application

This platform was built as a **proof-of-concept demonstration** and includes several shortcuts and simplifications. The following items **MUST** be addressed before production use:

### 1. **Security & Authentication** 🔒

**Current State (Demo)**:
- No authentication or authorization
- Hardcoded bearer token (`your-secret-token-123`)
- No user session management
- No role-based access control (RBAC)
- Simulated user data
- No audit logging

**Production Requirements**:
- ✅ Implement Azure AD / OAuth 2.0 authentication
- ✅ Add role-based access control (RBAC)
- ✅ Use Azure Key Vault for secrets management
- ✅ Implement proper session management
- ✅ Add multi-factor authentication (MFA)
- ✅ Implement comprehensive audit logging
- ✅ Add API rate limiting and throttling
- ✅ Implement certificate-based authentication for services
- ✅ Add IP whitelisting for sensitive endpoints
- ✅ Implement proper CORS policies

### 2. **Data & Storage** 💾

**Current State (Demo)**:
- All data is simulated/in-memory
- No persistent database
- No data encryption
- No backup strategy
- Events are randomly generated

**Production Requirements**:
- ✅ Implement persistent database (Azure SQL, CosmosDB)
- ✅ Add data encryption at rest and in transit
- ✅ Implement automated backup and disaster recovery
- ✅ Add data retention policies
- ✅ Implement GDPR/HIPAA compliance measures
- ✅ Add database connection pooling
- ✅ Implement data archival strategy
- ✅ Add point-in-time recovery capabilities

### 3. **Monitoring & Observability** 📊

**Current State (Demo)**:
- Basic console logging
- No centralized logging
- No metrics collection
- No alerting system
- No distributed tracing

**Production Requirements**:
- ✅ Implement Azure Application Insights
- ✅ Add centralized logging (Azure Log Analytics)
- ✅ Implement Prometheus/Grafana for metrics
- ✅ Add comprehensive alerting (Azure Monitor)
- ✅ Implement distributed tracing (OpenTelemetry)
- ✅ Add health check endpoints
- ✅ Implement SLA monitoring
- ✅ Add performance profiling
- ✅ Implement log aggregation and analysis

### 4. **High Availability & Scalability** 🚀

**Current State (Demo)**:
- Single replica deployments
- No load balancing
- No auto-scaling
- No geographic redundancy
- No failover mechanisms

**Production Requirements**:
- ✅ Implement multi-replica deployments (min 3)
- ✅ Add Azure Load Balancer / Application Gateway
- ✅ Implement Horizontal Pod Autoscaling (HPA)
- ✅ Add geographic redundancy (multi-region)
- ✅ Implement automatic failover
- ✅ Add circuit breakers and retry policies
- ✅ Implement database read replicas
- ✅ Add CDN for static assets
- ✅ Implement pod disruption budgets

### 5. **Network Security** 🌐

**Current State (Demo)**:
- Public endpoints
- No network segmentation
- No WAF
- No DDoS protection
- Basic network policies

**Production Requirements**:
- ✅ Implement Azure Private Link
- ✅ Add Web Application Firewall (WAF)
- ✅ Implement DDoS protection
- ✅ Add network segmentation (VNets, subnets)
- ✅ Implement Network Security Groups (NSGs)
- ✅ Add Azure Firewall
- ✅ Implement service mesh (Istio/Linkerd)
- ✅ Add egress filtering
- ✅ Implement zero-trust networking

### 6. **CI/CD & DevOps** 🔄

**Current State (Demo)**:
- Manual deployments
- No automated testing
- No deployment gates
- No rollback strategy
- No infrastructure as code

**Production Requirements**:
- ✅ Implement GitHub Actions / Azure DevOps pipelines
- ✅ Add automated unit, integration, and E2E tests
- ✅ Implement deployment gates and approvals
- ✅ Add blue-green or canary deployments
- ✅ Implement automated rollback
- ✅ Add infrastructure as code (Terraform/Bicep)
- ✅ Implement GitOps workflows
- ✅ Add security scanning in pipeline
- ✅ Implement artifact signing and verification

### 7. **Compliance & Governance** 📋

**Current State (Demo)**:
- No compliance controls
- No data classification
- No policy enforcement
- No compliance reporting

**Production Requirements**:
- ✅ Implement HIPAA compliance controls (healthcare data)
- ✅ Add SOC 2 compliance measures
- ✅ Implement data classification and labeling
- ✅ Add Azure Policy for governance
- ✅ Implement compliance reporting
- ✅ Add data residency controls
- ✅ Implement privacy controls (GDPR, CCPA)
- ✅ Add regulatory audit trails

### 8. **Error Handling & Resilience** 🛡️

**Current State (Demo)**:
- Basic error handling
- No retry logic
- No graceful degradation
- Limited error logging

**Production Requirements**:
- ✅ Implement comprehensive error handling
- ✅ Add exponential backoff retry logic
- ✅ Implement circuit breakers (Polly, Resilience4j)
- ✅ Add graceful degradation
- ✅ Implement dead letter queues
- ✅ Add chaos engineering practices
- ✅ Implement bulkhead patterns
- ✅ Add timeout policies

### 9. **Performance Optimization** ⚡

**Current State (Demo)**:
- No caching
- No query optimization
- No CDN
- No compression

**Production Requirements**:
- ✅ Implement Redis caching
- ✅ Add database query optimization
- ✅ Implement CDN (Azure CDN)
- ✅ Add response compression
- ✅ Implement lazy loading
- ✅ Add image optimization
- ✅ Implement connection pooling
- ✅ Add database indexing strategy

### 10. **Documentation & Training** 📖

**Current State (Demo)**:
- Basic README files
- Limited inline documentation
- No runbooks
- No training materials

**Production Requirements**:
- ✅ Create comprehensive API documentation
- ✅ Add architecture decision records (ADRs)
- ✅ Implement runbooks for common scenarios
- ✅ Create incident response procedures
- ✅ Add user training materials
- ✅ Implement knowledge base
- ✅ Add troubleshooting guides
- ✅ Create disaster recovery procedures

### 11. **Cost Management** 💵

**Current State (Demo)**:
- Basic auto-shutdown (15 min)
- No cost tracking
- No budget alerts
- No resource tagging

**Production Requirements**:
- ✅ Implement Azure Cost Management
- ✅ Add budget alerts and limits
- ✅ Implement resource tagging strategy
- ✅ Add cost allocation by team/project
- ✅ Implement reserved instances for predictable workloads
- ✅ Add spot instances for non-critical workloads
- ✅ Implement auto-scaling based on demand
- ✅ Add cost optimization recommendations

### 12. **Real Integrations** 🔌

**Current State (Demo)**:
- All integrations are simulated
- No real SIEM connections
- No actual EDR integration
- Mock API responses

**Production Requirements**:
- ✅ Implement real SIEM integration (Splunk, Sentinel)
- ✅ Add actual EDR platform connections
- ✅ Implement real ticketing system integration
- ✅ Add authentic identity provider integration
- ✅ Implement real-time threat intelligence feeds
- ✅ Add webhook integrations for notifications
- ✅ Implement bi-directional data sync

---

## 📁 Project Structure

```
McKesson_DevSecAutomation/
├── McKesson_SecurityAutomation_UI/  # Vue 3 SPA
│   ├── src/
│   │   ├── views/                 # Page components
│   │   ├── stores/                # Pinia state management
│   │   ├── router/                # Vue Router config
│   │   └── App.vue                # Root component
│   ├── package.json
│   └── vite.config.js
├── McKessonSimulatedApplications/
│   ├── HSPS/                      # Healthcare Provider System
│   │   ├── database-simulator/
│   │   ├── api-simulator/
│   │   ├── webui-simulator/
│   │   ├── security-portal/
│   │   └── deploy-hsps-to-aks.ps1
│   └── STAR/                      # Pharmacy System
│       ├── database-simulator/
│       ├── api-simulator/
│       ├── webui-simulator/
│       ├── security-portal/
│       └── deploy-star-to-aks.ps1
├── azure-function-pod-shutdown/   # Auto-shutdown function
│   ├── PodShutdownTimer/
│   │   ├── function.json
│   │   └── run.ps1
│   ├── host.json
│   └── profile.ps1
├── auto-shutdown-pods.ps1         # Manual shutdown script
├── AUTO-SHUTDOWN-README.md        # Shutdown documentation
├── AZURE-FUNCTION-SETUP-COMPLETE.md
├── .gitignore
└── README.md                      # This file
```

---

## 🤝 Contributing

This is a demonstration project. For production use, please fork and implement the production considerations listed above.

---

## 📄 License

This project is provided as-is for demonstration purposes.

---

## 🔗 Links

- **Live Demo**: https://mckessondemo-csutherland.azurewebsites.net
- **GitHub**: https://github.com/cs96ai/McKesson_SecurityAutomation
- **Azure Function**: https://hsps-pod-shutdown.azurewebsites.net

> **Note**: Azure subscription IDs and resource-specific URLs have been redacted from this documentation for security purposes.

---

## 📞 Support

For questions or issues with this demonstration:
- Open an issue on GitHub
- Contact: cs96ai@hotmail.com

---

**Built with ❤️ for demonstrating modern security automation practices**
