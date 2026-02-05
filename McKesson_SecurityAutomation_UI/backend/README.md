# Azure API Backend Server

Backend API service that provides secure, read-only access to Azure resources for the ChatOps interface.

## 🎯 Purpose

This Node.js/Express server acts as a secure intermediary between the Vue.js frontend and Azure APIs. It ensures that:
- All Azure API calls happen server-side (not in the browser)
- The read-only service principal credentials are never exposed to the frontend
- Only authenticated requests can access Azure data
- All operations are strictly read-only

## 🔒 Security Features

- **Read-Only Service Principal**: Uses Azure service principal with Reader role only
- **Bearer Token Authentication**: All API endpoints require valid bearer token
- **No Write Operations**: Physically impossible to modify Azure resources
- **Server-Side Only**: Azure credentials never sent to browser

## 📋 15 Read-Only Capabilities

1. **Get AKS Cluster Status** - `/api/azure/aks/status`
2. **List HSPS Pods** - `/api/azure/pods/hsps`
3. **List STAR Pods** - `/api/azure/pods/star`
4. **Get Pod Details** - `/api/azure/pods/:namespace/:podName`
5. **Get Resource Group Info** - `/api/azure/resourcegroup/:rgName`
6. **List All Resources** - `/api/azure/resources/list`
7. **Get App Service Status** - `/api/azure/appservice/:appName/status`
8. **Get Function App Status** - `/api/azure/functionapp/:functionName/status`
9. **Get Storage Account Info** - `/api/azure/storage/:accountName/info`
10. **Get AKS Node Pools** - `/api/azure/aks/nodepools`
11. **Get Deployment Status** - `/api/azure/deployments/:namespace`
12. **Get Service Status** - `/api/azure/services/:namespace`
13. **Get Pod Logs** - `/api/azure/pods/:namespace/:podName/logs`
14. **Get Subscription Info** - `/api/azure/subscription/info`
15. **Get Cost Analysis** - `/api/azure/costs/summary`

## 🚀 Setup

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Configure Environment

Copy the `.env.example` to `.env` in the parent directory:

```bash
# The backend reads from ../env (parent directory)
# Make sure these are set:

VITE_AZURE_TENANT_ID=33b0d***********************************
VITE_AZURE_CLIENT_ID=85336***********************************
VITE_AZURE_CLIENT_SECRET=gNu8Q*************************************
AZURE_SUBSCRIPTION_ID=3306e***********************************
VITE_BEARER_TOKEN=your-secret-token-123
```

### 3. Start the Server

**Development Mode** (with auto-reload):
```bash
npm run dev
```

**Production Mode**:
```bash
npm start
```

The server will start on `http://localhost:8000`

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Test AKS Status (requires authentication)
```bash
curl -H "Authorization: Bearer your-secret-token-123" \
     http://localhost:8000/api/azure/aks/status
```

### Test Pod Listing
```bash
curl -H "Authorization: Bearer your-secret-token-123" \
     http://localhost:8000/api/azure/pods/hsps
```

## 📊 API Response Format

All endpoints return JSON:

**Success Response**:
```json
{
  "name": "hsps-aks-cluster",
  "location": "eastus",
  "powerState": "Running",
  "kubernetesVersion": "1.27.7"
}
```

**Error Response**:
```json
{
  "error": "Error message here"
}
```

## 🔧 Dependencies

- **express**: Web server framework
- **cors**: Enable CORS for frontend communication
- **@azure/identity**: Azure authentication
- **@azure/arm-***: Azure Resource Management SDKs
- **@kubernetes/client-node**: Kubernetes API client
- **dotenv**: Environment variable management

## 🛡️ Security Notes

1. **Never expose this server publicly** - It should only be accessible from your Vue.js frontend
2. **Rotate bearer token regularly** - Change `VITE_BEARER_TOKEN` periodically
3. **Monitor access logs** - Track all API calls for security auditing
4. **Read-only guarantee** - The service principal physically cannot modify resources

## 📝 Integration with ChatOps

The Vue.js ChatOps interface calls this backend server to retrieve real Azure data:

1. User asks: "What's the status of the AKS cluster?"
2. Frontend detects Azure query
3. Frontend calls: `GET /api/azure/aks/status`
4. Backend authenticates request
5. Backend calls Azure API with read-only credentials
6. Backend returns data to frontend
7. OpenAI summarizes data for user

## 🔍 Troubleshooting

### "Unauthorized" Error
- Check that `VITE_BEARER_TOKEN` matches in both frontend and backend `.env` files

### "Azure API Error"
- Verify service principal credentials are correct
- Ensure service principal has Reader role on subscription
- Check that resources exist in the specified resource group

### "Cannot connect to Kubernetes"
- Verify AKS cluster is running
- Ensure service principal has access to AKS cluster credentials

## 📞 Support

For issues or questions:
- **GitHub**: https://github.com/cs96ai/McKesson_SecurityAutomation
- **Documentation**: See `CHATOPS-SECURITY-SETUP.md`
