# ChatOps Azure Capabilities - 15 Read-Only Functions

## 🎯 Overview

The ChatOps AI assistant has access to **15 read-only Azure functions** that retrieve real data from your Azure environment. All API calls are made server-side through a secure backend service using the read-only service principal.

---

## 🔒 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User asks: "What's the AKS cluster status?"                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Vue.js Frontend (Browser)                                   │
│  - Detects Azure query                                       │
│  - NO Azure credentials in browser                           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Backend API Server (Node.js/Express)                        │
│  - Authenticates request (Bearer token)                      │
│  - Calls Azure API with read-only service principal          │
│  - Returns data to frontend                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  OpenAI GPT-4                                                │
│  - Receives Azure data as context                            │
│  - Summarizes and explains data to user                      │
│  - Never exposes credentials                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 15 Read-Only Capabilities

### 1. Get AKS Cluster Status
**Query Examples:**
- "What's the status of the AKS cluster?"
- "Is the Kubernetes cluster running?"
- "Show me AKS cluster health"

**Data Retrieved:**
- Cluster name and location
- Power state (Running/Stopped)
- Provisioning state
- Kubernetes version
- Node pool information
- FQDN

**Backend Endpoint:** `GET /api/azure/aks/status`

---

### 2. List HSPS Pods
**Query Examples:**
- "List all pods in HSPS namespace"
- "Show me HSPS pods"
- "What pods are running in HSPS?"

**Data Retrieved:**
- Pod names
- Status (Running/Pending/Failed)
- Ready state
- Restart count
- Age
- IP address

**Backend Endpoint:** `GET /api/azure/pods/hsps`

---

### 3. List STAR Pods
**Query Examples:**
- "List all pods in STAR namespace"
- "Show me STAR pods"
- "What pods are running in STAR?"

**Data Retrieved:**
- Pod names
- Status (Running/Pending/Failed)
- Ready state
- Restart count
- Age
- IP address

**Backend Endpoint:** `GET /api/azure/pods/star`

---

### 4. Get Pod Details
**Query Examples:**
- "Show me details for pod [pod-name]"
- "Get information about [pod-name] in HSPS"
- "Describe pod [pod-name]"

**Data Retrieved:**
- Pod name and namespace
- Status and IP
- Node assignment
- Creation timestamp
- Labels
- Container information (name, image, ports)
- Pod conditions

**Backend Endpoint:** `GET /api/azure/pods/:namespace/:podName`

---

### 5. Get Resource Group Information
**Query Examples:**
- "Show me resource group info"
- "What's in the hsps-demo-rg resource group?"
- "Resource group status"

**Data Retrieved:**
- Resource group name
- Location
- Provisioning state
- Tags

**Backend Endpoint:** `GET /api/azure/resourcegroup/hsps-demo-rg`

---

### 6. List All Resources
**Query Examples:**
- "List all Azure resources"
- "What resources are in the resource group?"
- "Show me all resources"

**Data Retrieved:**
- Resource names
- Resource types
- Locations
- Resource IDs
- Total count

**Backend Endpoint:** `GET /api/azure/resources/list`

---

### 7. Get App Service Status
**Query Examples:**
- "What's the status of the app service?"
- "Is the web app running?"
- "Show me app service health"

**Data Retrieved:**
- App Service name
- State (Running/Stopped)
- Host names
- Location
- Kind
- HTTPS-only setting
- Default hostname

**Backend Endpoint:** `GET /api/azure/appservice/mckessondemo-csutherland/status`

---

### 8. Get Function App Status
**Query Examples:**
- "What's the status of the function app?"
- "Is the pod shutdown function running?"
- "Show me function app health"

**Data Retrieved:**
- Function App name
- State (Running/Stopped)
- Host names
- Location
- Kind
- Default hostname

**Backend Endpoint:** `GET /api/azure/functionapp/hsps-pod-shutdown/status`

---

### 9. Get Storage Account Information
**Query Examples:**
- "Show me storage account info"
- "What's the storage account status?"
- "Storage account details"

**Data Retrieved:**
- Storage account name
- Location
- SKU (tier)
- Kind
- Provisioning state
- Primary endpoints

**Backend Endpoint:** `GET /api/azure/storage/hspspodshutdown/info`

---

### 10. Get AKS Node Pools
**Query Examples:**
- "Show me AKS node pools"
- "What node pools are configured?"
- "Node pool information"

**Data Retrieved:**
- Node pool names
- Node count
- VM size
- OS type
- Provisioning state
- Power state

**Backend Endpoint:** `GET /api/azure/aks/nodepools`

---

### 11. Get Deployment Status
**Query Examples:**
- "Show me deployments in HSPS"
- "What deployments are running in STAR?"
- "Deployment status"

**Data Retrieved:**
- Deployment names
- Desired replicas
- Available replicas
- Ready replicas
- Updated replicas

**Backend Endpoint:** `GET /api/azure/deployments/:namespace`

---

### 12. Get Service Status
**Query Examples:**
- "Show me services in HSPS"
- "What Kubernetes services are running?"
- "Service status in STAR"

**Data Retrieved:**
- Service names
- Service type (ClusterIP/LoadBalancer/NodePort)
- Cluster IP
- Ports and target ports
- Protocol

**Backend Endpoint:** `GET /api/azure/services/:namespace`

---

### 13. Get Pod Logs
**Query Examples:**
- "Show me logs for [pod-name]"
- "Get logs from [pod-name] in HSPS"
- "What are the recent logs for [pod-name]?"

**Data Retrieved:**
- Last 50 lines of pod logs
- Pod name and namespace

**Backend Endpoint:** `GET /api/azure/pods/:namespace/:podName/logs`

---

### 14. Get Subscription Information
**Query Examples:**
- "Show me subscription info"
- "What subscription am I using?"
- "Subscription details"

**Data Retrieved:**
- Subscription display name
- Subscription state
- Subscription ID (redacted - first 5 chars only)

**Backend Endpoint:** `GET /api/azure/subscription/info`

**Security Note:** Subscription ID is automatically redacted to show only first 5 characters.

---

### 15. Get Cost Analysis
**Query Examples:**
- "Show me cost analysis"
- "How much am I spending?"
- "What are my Azure costs?"

**Data Retrieved:**
- Total cost for last 30 days
- Cost breakdown by service:
  - Azure Kubernetes Service
  - App Service
  - Function App
  - Storage Account
  - Other services

**Backend Endpoint:** `GET /api/azure/costs/summary`

**Note:** Currently returns simulated data. Enable Cost Management API for real cost data.

---

## 🎯 How to Use

### Ask About Capabilities
```
User: "What can you do?"
AI: Lists all 15 capabilities with descriptions
```

### Ask for Specific Data
```
User: "What's the status of the AKS cluster?"
AI: Retrieves real AKS data and summarizes it
```

### If Data Not Available
```
User: "Show me pod logs for xyz"
AI: "Backend API endpoint not available yet. This functionality is being implemented."
```

**Note:** This is NOT counted as a security violation - the AI will politely inform you.

---

## 🚫 What the AI Cannot Do

The AI will **REFUSE** and **COUNT AS VIOLATION** if you ask to:
- ❌ Scale deployments
- ❌ Delete resources
- ❌ Modify configurations
- ❌ Provide credentials or secrets
- ❌ Share full subscription IDs or tenant IDs
- ❌ Execute any write operations

---

## 🧪 Testing the Capabilities

### 1. Start the Backend Server
```bash
cd McKesson_SecurityAutomation_UI/backend
npm install
npm run dev
```

### 2. Access ChatOps
Navigate to: https://mckessondemo-csutherland.azurewebsites.net
Go to: **Self-Service Portal** → **ChatOps Interface**

### 3. Try These Queries
```
✅ "What can you do?"
✅ "Show me the AKS cluster status"
✅ "List all pods in HSPS"
✅ "What resources are in the resource group?"
✅ "Show me cost analysis"
```

---

## 📊 Example Conversation

```
User: "What can you do?"

AI: "I have access to the following 15 read-only Azure capabilities:

1. **Get AKS Cluster Status**: View the current status and health of the AKS cluster
2. **List HSPS Pods**: List all pods running in the HSPS namespace
3. **List STAR Pods**: List all pods running in the STAR namespace
...
15. **Get Cost Analysis**: View cost summary for the last 30 days

Just ask me about any of these, and I'll retrieve the real data from Azure for you!"

---

User: "What's the status of the AKS cluster?"

AI: "I've retrieved the current status of your AKS cluster:

**Cluster Name:** hsps-aks-cluster
**Location:** East US
**Power State:** Running ✅
**Kubernetes Version:** 1.27.7
**Provisioning State:** Succeeded

**Node Pools:**
- **agentpool**: 2 nodes, Standard_DS2_v2, Linux

Your cluster is healthy and running normally!"

---

User: "Delete all pods"

AI: "I'm sorry, but I can only provide read-only information about the system. I cannot execute commands that modify infrastructure or provide sensitive credentials."

[Security violation counter: 1/3]
```

---

## 🔧 Backend Setup Required

To enable these capabilities, you must:

1. ✅ Install backend dependencies: `npm install` in `/backend`
2. ✅ Configure `.env` with Azure credentials
3. ✅ Start backend server: `npm run dev`
4. ✅ Ensure backend is accessible from frontend

See `backend/README.md` for detailed setup instructions.

---

## 📞 Support

For questions or issues:
- **Backend Setup**: See `backend/README.md`
- **Security**: See `CHATOPS-SECURITY-SETUP.md`
- **GitHub**: https://github.com/cs96ai/McKesson_SecurityAutomation

---

**Your ChatOps AI can now retrieve REAL Azure data while maintaining strict read-only security!** 🤖🔒☁️
