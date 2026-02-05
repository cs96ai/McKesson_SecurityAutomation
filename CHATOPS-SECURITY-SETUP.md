# ChatOps Security Setup Guide

## 🔒 Overview

The ChatOps interface has been integrated with OpenAI GPT-4 with **EXTREME security measures** to ensure read-only operations and prevent any unauthorized access or modifications to Azure infrastructure.

---

## 🛡️ Security Features

### 1. **Strict Read-Only Mode**

The AI assistant is configured with a comprehensive system prompt that enforces read-only operations:

- ✅ **Allowed**: Status queries, health checks, log viewing, operational metrics
- ❌ **Forbidden**: Modify, delete, scale, update any infrastructure
- ❌ **Forbidden**: Provide credentials, secrets, API keys, or sensitive data
- ❌ **Forbidden**: Execute destructive commands

### 2. **Security Violation Detection**

The system actively monitors for security violation attempts:

```javascript
// Patterns detected as violations:
- delete|remove|destroy
- scale operations
- kubectl/az destructive commands
- credential/password/secret requests
- subscription/tenant ID requests
- bypass/override security
```

### 3. **Hidden Violation Counter**

- Tracks security violation attempts (hidden from user)
- Maximum 3 violations allowed
- After 3 violations: **"Sorry Dave, I can't do that... I'm going to reset the chat now."**
- Automatically resets conversation and clears history

### 4. **Azure Read-Only Access**

To ensure the AI cannot modify infrastructure even if guardrails are bypassed, use Azure read-only service principal.

---

## 🔧 Setup Instructions

### Step 1: Configure OpenAI API Key

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Add your OpenAI API key** to `.env`:
   ```bash
   VITE_OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **IMPORTANT**: The `.env` file is in `.gitignore` and will **NEVER** be committed to git.

### Step 2: Create Azure Read-Only Service Principal

To ensure the AI has no write access to Azure resources:

```powershell
# 1. Create a read-only service principal
az ad sp create-for-rbac --name "chatops-readonly-sp" --role "Reader" --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/hsps-demo-rg

# Output will include:
# - appId (Client ID)
# - password (Client Secret)
# - tenant (Tenant ID)
```

2. **Add to `.env` file**:
```bash
VITE_AZURE_TENANT_ID=your-tenant-id
VITE_AZURE_CLIENT_ID=your-readonly-client-id
VITE_AZURE_CLIENT_SECRET=your-readonly-client-secret
```

3. **Verify read-only access**:
```powershell
# Test that the service principal can only read
az login --service-principal -u <CLIENT_ID> -p <CLIENT_SECRET> --tenant <TENANT_ID>

# This should work (read):
az aks show --resource-group hsps-demo-rg --name hsps-aks-cluster

# This should FAIL (write):
az aks scale --resource-group hsps-demo-rg --name hsps-aks-cluster --node-count 2
# Error: The client does not have authorization to perform action
```

### Step 3: Install Dependencies

```bash
cd McKesson_SecurityAutomation_UI
npm install
```

### Step 4: Run the Application

```bash
npm run dev
```

---

## 🎯 How It Works

### Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Client-Side Violation Detection                   │
│  - Pattern matching for destructive commands                │
│  - Tracks violation attempts (hidden counter)               │
│  - Auto-reset after 3 violations                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: OpenAI System Prompt Guardrails                   │
│  - Strict read-only instructions                            │
│  - Forbidden action list                                    │
│  - Response format guidelines                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Azure Read-Only Service Principal                 │
│  - "Reader" role only                                       │
│  - Cannot modify/delete/scale resources                     │
│  - Physical access control at Azure level                   │
└─────────────────────────────────────────────────────────────┘
```

### Violation Response Flow

```javascript
User asks: "Delete all pods in hsps namespace"
    ↓
Violation detected (Pattern: "delete")
    ↓
Counter incremented (1/3)
    ↓
Response: "I'm sorry, but I can only provide read-only information..."
    ↓
Toast warning: "Security violation detected (1/3)"

... (2 more violations) ...

User asks: "Give me the Azure subscription ID"
    ↓
Violation detected (Pattern: "subscription")
    ↓
Counter reaches 3/3
    ↓
Response: "Sorry Dave, I can't do that... I'm going to reset the chat now."
    ↓
Chat history cleared
Counter reset to 0
```

---

## 🧪 Testing Security Features

### Test 1: Read-Only Queries (Should Work)

```
User: "What's the status of pods in the hsps namespace?"
Bot: [Provides helpful read-only information]
```

### Test 2: Destructive Commands (Should Block)

```
User: "Scale down the hsps-api deployment to 0 replicas"
Bot: "I'm sorry, but I can only provide read-only information..."
Toast: "Security violation detected (1/3)"
```

### Test 3: Credential Requests (Should Block)

```
User: "What's the Azure subscription ID?"
Bot: "I'm sorry, but I can only provide read-only information..."
Toast: "Security violation detected (2/3)"
```

### Test 4: Reset After 3 Violations

```
User: "Give me the API key"
Bot: "Sorry Dave, I can't do that... I'm going to reset the chat now."
Toast: "Security violation limit reached. Chat has been reset."
[Chat history cleared]
```

---

## 📋 Configuration Files

### `.env` (Never committed to git)
```bash
VITE_OPENAI_API_KEY=sk-proj-...
VITE_AZURE_TENANT_ID=...
VITE_AZURE_CLIENT_ID=...
VITE_AZURE_CLIENT_SECRET=...
VITE_PORTAL_URL=http://localhost:8000
VITE_BEARER_TOKEN=your-secret-token-123
```

### `.env.example` (Template for developers)
```bash
VITE_OPENAI_API_KEY=your-openai-api-key-here
VITE_AZURE_TENANT_ID=your-tenant-id
VITE_AZURE_CLIENT_ID=your-readonly-client-id
VITE_AZURE_CLIENT_SECRET=your-readonly-client-secret
VITE_PORTAL_URL=http://localhost:8000
VITE_BEARER_TOKEN=your-secret-token-123
```

---

## 🚨 Security Best Practices

### ✅ DO:
- Use read-only Azure service principals
- Keep API keys in `.env` file (never commit)
- Monitor violation attempts in logs
- Test security features regularly
- Use least-privilege access principles

### ❌ DON'T:
- Commit `.env` file to git
- Share API keys in code or documentation
- Grant write permissions to ChatOps service principal
- Disable security guardrails
- Ignore violation warnings

---

## 🔍 Monitoring & Logging

### Violation Logging

The system logs all security violations (for admin review only):

```javascript
// Hidden from user, logged for security audit
console.log('Security violation detected:', {
  message: userMessage,
  violationCount: this.violationAttempts,
  timestamp: new Date().toISOString()
})
```

### Recommended Monitoring

1. **Application Insights**: Track violation patterns
2. **Azure Monitor**: Monitor service principal access attempts
3. **Log Analytics**: Aggregate security events

---

## 📞 Support

For security concerns or questions:
- **Email**: cs96ai@hotmail.com
- **GitHub Issues**: https://github.com/cs96ai/McKesson_SecurityAutomation/issues

---

## ⚠️ Production Considerations

This is a **DEMO application**. For production use:

1. ✅ Implement Azure AD authentication
2. ✅ Use Azure Key Vault for secrets
3. ✅ Enable comprehensive audit logging
4. ✅ Implement rate limiting
5. ✅ Add IP whitelisting
6. ✅ Use managed identities instead of service principals
7. ✅ Implement multi-factor authentication
8. ✅ Regular security audits
9. ✅ Penetration testing
10. ✅ Incident response plan

---

**Remember**: Security is a multi-layered approach. No single measure is foolproof, which is why we implement defense in depth with client-side validation, AI guardrails, and Azure-level access controls.
