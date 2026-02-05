/**
 * Backend API Server for Azure Read-Only Operations
 * 
 * This Express server provides secure backend endpoints for Azure API calls.
 * Uses the read-only service principal to ensure no write operations are possible.
 */

const express = require('express')
const cors = require('cors')
const { DefaultAzureCredential, ClientSecretCredential } = require('@azure/identity')
const { ResourceManagementClient } = require('@azure/arm-resources')
const { ContainerServiceClient } = require('@azure/arm-containerservice')
const { WebSiteManagementClient } = require('@azure/arm-appservice')
const { StorageManagementClient } = require('@azure/arm-storage')
const { CostManagementClient } = require('@azure/arm-costmanagement')
const k8s = require('@kubernetes/client-node')

require('dotenv').config({ path: '../.env' })

const app = express()
const PORT = process.env.PORT || 8000

// Middleware
app.use(cors())
app.use(express.json())

// Azure Configuration
const SUBSCRIPTION_ID = process.env.AZURE_SUBSCRIPTION_ID || '3306e559-a033-43dd-bf98-fc59174d563f'
const RESOURCE_GROUP = 'hsps-demo-rg'
const AKS_CLUSTER_NAME = 'hsps-aks-cluster'

// Initialize Azure credentials (read-only service principal)
const credential = new ClientSecretCredential(
  process.env.VITE_AZURE_TENANT_ID,
  process.env.VITE_AZURE_CLIENT_ID,
  process.env.VITE_AZURE_CLIENT_SECRET
)

// Initialize Azure clients
const resourceClient = new ResourceManagementClient(credential, SUBSCRIPTION_ID)
const aksClient = new ContainerServiceClient(credential, SUBSCRIPTION_ID)
const webClient = new WebSiteManagementClient(credential, SUBSCRIPTION_ID)
const storageClient = new StorageManagementClient(credential, SUBSCRIPTION_ID)

// Bearer token authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization']
  const token = authHeader && authHeader.split(' ')[1]

  if (!token || token !== process.env.VITE_BEARER_TOKEN) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  next()
}

// Apply authentication to all /api routes
app.use('/api', authenticateToken)

// ============================================================================
// 1. Get AKS Cluster Status
// ============================================================================
app.get('/api/azure/aks/status', async (req, res) => {
  try {
    const cluster = await aksClient.managedClusters.get(RESOURCE_GROUP, AKS_CLUSTER_NAME)
    
    res.json({
      name: cluster.name,
      location: cluster.location,
      powerState: cluster.powerState?.code || 'Unknown',
      provisioningState: cluster.provisioningState,
      kubernetesVersion: cluster.kubernetesVersion,
      nodeResourceGroup: cluster.nodeResourceGroup,
      fqdn: cluster.fqdn,
      agentPoolProfiles: cluster.agentPoolProfiles?.map(pool => ({
        name: pool.name,
        count: pool.count,
        vmSize: pool.vmSize,
        osType: pool.osType
      }))
    })
  } catch (error) {
    console.error('Error fetching AKS status:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 2 & 3. List Pods in HSPS/STAR Namespace
// ============================================================================
app.get('/api/azure/pods/:namespace', async (req, res) => {
  try {
    const { namespace } = req.params
    
    // Get AKS credentials
    const credentials = await aksClient.managedClusters.listClusterUserCredentials(
      RESOURCE_GROUP,
      AKS_CLUSTER_NAME
    )
    
    // Configure kubectl
    const kc = new k8s.KubeConfig()
    const kubeconfig = Buffer.from(credentials.kubeconfigs[0].value).toString()
    kc.loadFromString(kubeconfig)
    
    const k8sApi = kc.makeApiClient(k8s.CoreV1Api)
    const podsResponse = await k8sApi.listNamespacedPod(namespace)
    
    const pods = podsResponse.body.items.map(pod => ({
      name: pod.metadata.name,
      status: pod.status.phase,
      ready: pod.status.containerStatuses?.every(c => c.ready) || false,
      restarts: pod.status.containerStatuses?.reduce((sum, c) => sum + c.restartCount, 0) || 0,
      age: calculateAge(pod.metadata.creationTimestamp),
      ip: pod.status.podIP
    }))
    
    res.json({ namespace, pods, count: pods.length })
  } catch (error) {
    console.error('Error fetching pods:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 4. Get Pod Details
// ============================================================================
app.get('/api/azure/pods/:namespace/:podName', async (req, res) => {
  try {
    const { namespace, podName } = req.params
    
    const credentials = await aksClient.managedClusters.listClusterUserCredentials(
      RESOURCE_GROUP,
      AKS_CLUSTER_NAME
    )
    
    const kc = new k8s.KubeConfig()
    const kubeconfig = Buffer.from(credentials.kubeconfigs[0].value).toString()
    kc.loadFromString(kubeconfig)
    
    const k8sApi = kc.makeApiClient(k8s.CoreV1Api)
    const podResponse = await k8sApi.readNamespacedPod(podName, namespace)
    const pod = podResponse.body
    
    res.json({
      name: pod.metadata.name,
      namespace: pod.metadata.namespace,
      status: pod.status.phase,
      ip: pod.status.podIP,
      node: pod.spec.nodeName,
      creationTimestamp: pod.metadata.creationTimestamp,
      labels: pod.metadata.labels,
      containers: pod.spec.containers.map(c => ({
        name: c.name,
        image: c.image,
        ports: c.ports
      })),
      conditions: pod.status.conditions
    })
  } catch (error) {
    console.error('Error fetching pod details:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 5. Get Resource Group Information
// ============================================================================
app.get('/api/azure/resourcegroup/:rgName', async (req, res) => {
  try {
    const { rgName } = req.params
    const rg = await resourceClient.resourceGroups.get(rgName)
    
    res.json({
      name: rg.name,
      location: rg.location,
      provisioningState: rg.properties.provisioningState,
      tags: rg.tags
    })
  } catch (error) {
    console.error('Error fetching resource group:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 6. List All Resources
// ============================================================================
app.get('/api/azure/resources/list', async (req, res) => {
  try {
    const resources = []
    for await (const resource of resourceClient.resources.listByResourceGroup(RESOURCE_GROUP)) {
      resources.push({
        name: resource.name,
        type: resource.type,
        location: resource.location,
        id: resource.id
      })
    }
    
    res.json({ resourceGroup: RESOURCE_GROUP, resources, count: resources.length })
  } catch (error) {
    console.error('Error listing resources:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 7. Get App Service Status
// ============================================================================
app.get('/api/azure/appservice/:appName/status', async (req, res) => {
  try {
    const { appName } = req.params
    const app = await webClient.webApps.get(RESOURCE_GROUP, appName)
    
    res.json({
      name: app.name,
      state: app.state,
      hostNames: app.hostNames,
      location: app.location,
      kind: app.kind,
      httpsOnly: app.httpsOnly,
      defaultHostName: app.defaultHostName
    })
  } catch (error) {
    console.error('Error fetching app service:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 8. Get Function App Status
// ============================================================================
app.get('/api/azure/functionapp/:functionName/status', async (req, res) => {
  try {
    const { functionName } = req.params
    const functionApp = await webClient.webApps.get(RESOURCE_GROUP, functionName)
    
    res.json({
      name: functionApp.name,
      state: functionApp.state,
      hostNames: functionApp.hostNames,
      location: functionApp.location,
      kind: functionApp.kind,
      defaultHostName: functionApp.defaultHostName
    })
  } catch (error) {
    console.error('Error fetching function app:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 9. Get Storage Account Information
// ============================================================================
app.get('/api/azure/storage/:accountName/info', async (req, res) => {
  try {
    const { accountName } = req.params
    const account = await storageClient.storageAccounts.getProperties(RESOURCE_GROUP, accountName)
    
    res.json({
      name: account.name,
      location: account.location,
      sku: account.sku,
      kind: account.kind,
      provisioningState: account.provisioningState,
      primaryEndpoints: account.primaryEndpoints
    })
  } catch (error) {
    console.error('Error fetching storage account:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 10. Get AKS Node Pools
// ============================================================================
app.get('/api/azure/aks/nodepools', async (req, res) => {
  try {
    const nodePools = []
    for await (const pool of aksClient.agentPools.list(RESOURCE_GROUP, AKS_CLUSTER_NAME)) {
      nodePools.push({
        name: pool.name,
        count: pool.count,
        vmSize: pool.vmSize,
        osType: pool.osType,
        provisioningState: pool.provisioningState,
        powerState: pool.powerState?.code
      })
    }
    
    res.json({ nodePools, count: nodePools.length })
  } catch (error) {
    console.error('Error fetching node pools:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 11. Get Deployment Status
// ============================================================================
app.get('/api/azure/deployments/:namespace', async (req, res) => {
  try {
    const { namespace } = req.params
    
    const credentials = await aksClient.managedClusters.listClusterUserCredentials(
      RESOURCE_GROUP,
      AKS_CLUSTER_NAME
    )
    
    const kc = new k8s.KubeConfig()
    const kubeconfig = Buffer.from(credentials.kubeconfigs[0].value).toString()
    kc.loadFromString(kubeconfig)
    
    const k8sApi = kc.makeApiClient(k8s.AppsV1Api)
    const deploymentsResponse = await k8sApi.listNamespacedDeployment(namespace)
    
    const deployments = deploymentsResponse.body.items.map(dep => ({
      name: dep.metadata.name,
      replicas: dep.spec.replicas,
      availableReplicas: dep.status.availableReplicas || 0,
      readyReplicas: dep.status.readyReplicas || 0,
      updatedReplicas: dep.status.updatedReplicas || 0
    }))
    
    res.json({ namespace, deployments, count: deployments.length })
  } catch (error) {
    console.error('Error fetching deployments:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 12. Get Service Status
// ============================================================================
app.get('/api/azure/services/:namespace', async (req, res) => {
  try {
    const { namespace } = req.params
    
    const credentials = await aksClient.managedClusters.listClusterUserCredentials(
      RESOURCE_GROUP,
      AKS_CLUSTER_NAME
    )
    
    const kc = new k8s.KubeConfig()
    const kubeconfig = Buffer.from(credentials.kubeconfigs[0].value).toString()
    kc.loadFromString(kubeconfig)
    
    const k8sApi = kc.makeApiClient(k8s.CoreV1Api)
    const servicesResponse = await k8sApi.listNamespacedService(namespace)
    
    const services = servicesResponse.body.items.map(svc => ({
      name: svc.metadata.name,
      type: svc.spec.type,
      clusterIP: svc.spec.clusterIP,
      ports: svc.spec.ports?.map(p => ({ port: p.port, targetPort: p.targetPort, protocol: p.protocol }))
    }))
    
    res.json({ namespace, services, count: services.length })
  } catch (error) {
    console.error('Error fetching services:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 13. Get Pod Logs
// ============================================================================
app.get('/api/azure/pods/:namespace/:podName/logs', async (req, res) => {
  try {
    const { namespace, podName } = req.params
    
    const credentials = await aksClient.managedClusters.listClusterUserCredentials(
      RESOURCE_GROUP,
      AKS_CLUSTER_NAME
    )
    
    const kc = new k8s.KubeConfig()
    const kubeconfig = Buffer.from(credentials.kubeconfigs[0].value).toString()
    kc.loadFromString(kubeconfig)
    
    const k8sApi = kc.makeApiClient(k8s.CoreV1Api)
    const logsResponse = await k8sApi.readNamespacedPodLog(
      podName,
      namespace,
      undefined, // container
      false, // follow
      undefined, // insecureSkipTLSVerifyBackend
      undefined, // limitBytes
      undefined, // pretty
      undefined, // previous
      undefined, // sinceSeconds
      50, // tailLines
      undefined // timestamps
    )
    
    const logs = logsResponse.body.split('\n').slice(-50)
    
    res.json({ podName, namespace, logs })
  } catch (error) {
    console.error('Error fetching pod logs:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 14. Get Subscription Information (Non-Sensitive)
// ============================================================================
app.get('/api/azure/subscription/info', async (req, res) => {
  try {
    const subscription = await resourceClient.subscriptions.get(SUBSCRIPTION_ID)
    
    res.json({
      displayName: subscription.displayName,
      state: subscription.state,
      subscriptionId: `${SUBSCRIPTION_ID.substring(0, 5)}***********************************`
    })
  } catch (error) {
    console.error('Error fetching subscription:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// 15. Get Cost Analysis (Simulated - requires Cost Management API setup)
// ============================================================================
app.get('/api/azure/costs/summary', async (req, res) => {
  try {
    // Note: Cost Management API requires additional setup and permissions
    // For now, returning simulated data
    res.json({
      period: 'Last 30 days',
      totalCost: '$127.45',
      breakdown: [
        { service: 'Azure Kubernetes Service', cost: '$45.20' },
        { service: 'App Service', cost: '$32.10' },
        { service: 'Function App', cost: '$15.80' },
        { service: 'Storage Account', cost: '$12.35' },
        { service: 'Other', cost: '$22.00' }
      ],
      note: 'Cost data is simulated. Enable Cost Management API for real data.'
    })
  } catch (error) {
    console.error('Error fetching costs:', error)
    res.status(500).json({ error: error.message })
  }
})

// ============================================================================
// Helper Functions
// ============================================================================
function calculateAge(timestamp) {
  const now = new Date()
  const created = new Date(timestamp)
  const diffMs = now - created
  const diffMins = Math.floor(diffMs / 60000)
  
  if (diffMins < 60) return `${diffMins}m`
  const diffHours = Math.floor(diffMins / 60)
  if (diffHours < 24) return `${diffHours}h`
  const diffDays = Math.floor(diffHours / 24)
  return `${diffDays}d`
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() })
})

// Start server
app.listen(PORT, () => {
  console.log(`Azure API Backend running on port ${PORT}`)
  console.log(`Health check: http://localhost:${PORT}/health`)
})
