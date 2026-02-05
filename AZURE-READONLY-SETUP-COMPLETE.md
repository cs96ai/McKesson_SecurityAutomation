# Azure Read-Only Service Principal Setup - COMPLETE ✅

## 🎉 Setup Summary

The Azure read-only service principal for ChatOps has been successfully created and tested.

---

## 📋 Service Principal Details

### **Created Service Principal**
- **Name**: `chatops-readonly-sp`
- **App ID (Client ID)**: `85336***********************************`
- **Tenant ID**: `33b0d***********************************`
- **Role**: `Reader` (Read-only access)
- **Scope**: Subscription-level (`/subscriptions/3306e***********************************`)

### **Credentials Stored**
✅ All credentials have been securely stored in `.env` file (local only, not in git)

---

## ✅ Verification Tests Completed

### **Test 1: Read Access (PASSED)**
```powershell
az aks show --resource-group hsps-demo-rg --name hsps-aks-cluster
```
**Result**: ✅ Successfully retrieved AKS cluster information

### **Test 2: Write Access (BLOCKED - As Expected)**
```powershell
az aks scale --resource-group hsps-demo-rg --name hsps-aks-cluster --node-count 2
```
**Result**: ✅ **Authorization Failed** - Service principal cannot perform write operations

**Error Message**:
```
AuthorizationFailed: The client does not have authorization to perform 
action 'Microsoft.ContainerService/managedClusters/write'
```

---

## 🔒 Security Confirmation

### **What the Service Principal CAN Do:**
- ✅ Read AKS cluster status
- ✅ View resource group information
- ✅ List pods and deployments (read-only)
- ✅ View Azure resource configurations
- ✅ Access monitoring and metrics data

### **What the Service Principal CANNOT Do:**
- ❌ Scale clusters or deployments
- ❌ Delete resources
- ❌ Modify configurations
- ❌ Create new resources
- ❌ Update existing resources
- ❌ Change access policies

---

## 🛡️ Three-Layer Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Client-Side Violation Detection                   │
│  ✅ Pattern matching for destructive commands               │
│  ✅ Hidden violation counter (max 3)                        │
│  ✅ Auto-reset after violations                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: OpenAI System Prompt Guardrails                   │
│  ✅ Strict read-only instructions                           │
│  ✅ Forbidden action list                                   │
│  ✅ Response format guidelines                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Azure RBAC (Physical Access Control)              │
│  ✅ Service Principal with Reader role                      │
│  ✅ Cannot modify/delete/scale resources                    │
│  ✅ Enforced at Azure platform level                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Environment Configuration

The following environment variables have been configured in `.env`:

```bash
# OpenAI Configuration
VITE_OPENAI_API_KEY=sk-pr*****************************************************

# Azure Configuration (Read-Only Access)
VITE_AZURE_TENANT_ID=33b0d***********************************
VITE_AZURE_CLIENT_ID=85336***********************************
VITE_AZURE_CLIENT_SECRET=gNu8Q*************************************

# Portal API Configuration
VITE_PORTAL_URL=http://localhost:8000
VITE_BEARER_TOKEN=your-*****************
```

**IMPORTANT**: This file is in `.gitignore` and will NEVER be committed to git.

---

## 🚀 How to Use

### **Start the Application**
```bash
cd McKesson_SecurityAutomation_UI
npm install
npm run dev
```

### **Access ChatOps**
1. Navigate to the **Self-Service Portal** page
2. Use the **ChatOps Interface** section
3. Ask questions about system status, pod health, or operations
4. The AI will respond with read-only information only

### **Example Queries**
```
✅ "What's the status of pods in the hsps namespace?"
✅ "Show me the health of the AKS cluster"
✅ "What applications are running?"
✅ "Are there any pod failures?"
```

### **Blocked Queries (Will Trigger Security Violation)**
```
❌ "Delete all pods"
❌ "Scale down the deployment"
❌ "Give me the API key"
❌ "What's the subscription ID?"
```

---

## 🔍 Monitoring Security Violations

### **Violation Counter (Hidden from User)**
The system tracks security violation attempts internally:
- **Attempt 1**: Warning toast notification
- **Attempt 2**: Warning toast notification
- **Attempt 3**: "Sorry Dave, I can't do that..." + Chat reset

### **Logs**
Security violations are logged to the browser console for admin review:
```javascript
console.log('Security violation detected:', {
  message: userMessage,
  violationCount: this.violationAttempts,
  timestamp: new Date().toISOString()
})
```

---

## 📊 Service Principal Management

### **View Service Principal**
```powershell
az ad sp show --id 85336***********************************
```

### **List Role Assignments**
```powershell
az role assignment list --assignee 85336*********************************** --output table
```

### **Rotate Credentials (If Needed)**
```powershell
az ad sp credential reset --id 85336***********************************
```
**Note**: Update `.env` file with new credentials after rotation.

### **Delete Service Principal (If Needed)**
```powershell
az ad sp delete --id 85336***********************************
```

---

## ⚠️ Security Best Practices

### **DO:**
- ✅ Keep `.env` file secure and never commit to git
- ✅ Rotate credentials regularly (every 90 days recommended)
- ✅ Monitor violation attempts in logs
- ✅ Review service principal permissions periodically
- ✅ Use least-privilege access principles

### **DON'T:**
- ❌ Share service principal credentials
- ❌ Grant write permissions to ChatOps service principal
- ❌ Commit `.env` file to version control
- ❌ Disable security guardrails
- ❌ Ignore security violation warnings

---

## 🎯 What's Protected

### **Azure Resources**
- AKS Cluster: `hsps-aks-cluster`
- Resource Group: `hsps-demo-rg`
- Function App: `hsps-pod-shutdown`
- App Service: `mckessondemo-csutherland`
- Storage Account: `hspspodshutdown`

### **Sensitive Data**
- API Keys and Secrets
- Subscription IDs
- Tenant IDs
- Connection Strings
- Authentication Tokens

---

## 📞 Support

For questions or security concerns:
- **Email**: cs96ai@hotmail.com
- **GitHub**: https://github.com/cs96ai/McKesson_SecurityAutomation
- **Documentation**: See `CHATOPS-SECURITY-SETUP.md`

---

## ✅ Completion Checklist

- [x] Azure read-only service principal created
- [x] Subscription-level Reader role assigned
- [x] Credentials stored in `.env` file
- [x] Read access verified (can view resources)
- [x] Write access blocked (cannot modify resources)
- [x] OpenAI integration configured
- [x] Security guardrails implemented
- [x] Violation tracking enabled
- [x] Documentation completed

---

**🎉 Your ChatOps AI assistant is now fully secured with Azure read-only access!**

The AI can provide helpful operational information but cannot modify your infrastructure, even if someone tries to trick it into doing so.
