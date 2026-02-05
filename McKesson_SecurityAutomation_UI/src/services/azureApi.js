/**
 * Azure API Service - Backend Integration Layer
 * 
 * This service provides 15 read-only Azure functionalities that can be called
 * through the ChatOps interface. All Azure API calls are made server-side for security.
 * 
 * Uses the read-only service principal with Reader role.
 */

import { config } from '../config/env'

const BACKEND_API_URL = config.portal.url || 'http://localhost:8000'

/**
 * 15 Read-Only Azure Functionalities
 */
export const azureFunctions = {
  // 1. Get AKS Cluster Status
  getAksClusterStatus: async () => {
    return await callBackendApi('/api/azure/aks/status')
  },

  // 2. List All Pods in HSPS Namespace
  listHspsPods: async () => {
    return await callBackendApi('/api/azure/pods/hsps')
  },

  // 3. List All Pods in STAR Namespace
  listStarPods: async () => {
    return await callBackendApi('/api/azure/pods/star')
  },

  // 4. Get Pod Details by Name
  getPodDetails: async (namespace, podName) => {
    return await callBackendApi(`/api/azure/pods/${namespace}/${podName}`)
  },

  // 5. Get Resource Group Information
  getResourceGroupInfo: async () => {
    return await callBackendApi('/api/azure/resourcegroup/hsps-demo-rg')
  },

  // 6. List All Azure Resources in Resource Group
  listAllResources: async () => {
    return await callBackendApi('/api/azure/resources/list')
  },

  // 7. Get App Service Status
  getAppServiceStatus: async () => {
    return await callBackendApi('/api/azure/appservice/mckessondemo-csutherland/status')
  },

  // 8. Get Function App Status
  getFunctionAppStatus: async () => {
    return await callBackendApi('/api/azure/functionapp/hsps-pod-shutdown/status')
  },

  // 9. Get Storage Account Information
  getStorageAccountInfo: async () => {
    return await callBackendApi('/api/azure/storage/hspspodshutdown/info')
  },

  // 10. Get AKS Node Pool Information
  getAksNodePools: async () => {
    return await callBackendApi('/api/azure/aks/nodepools')
  },

  // 11. Get Deployment Status in Namespace
  getDeploymentStatus: async (namespace) => {
    return await callBackendApi(`/api/azure/deployments/${namespace}`)
  },

  // 12. Get Service Status in Namespace
  getServiceStatus: async (namespace) => {
    return await callBackendApi(`/api/azure/services/${namespace}`)
  },

  // 13. Get Pod Logs (Last 50 Lines)
  getPodLogs: async (namespace, podName) => {
    return await callBackendApi(`/api/azure/pods/${namespace}/${podName}/logs`)
  },

  // 14. Get Azure Subscription Information
  getSubscriptionInfo: async () => {
    return await callBackendApi('/api/azure/subscription/info')
  },

  // 15. Get Cost Analysis Summary (Last 30 Days)
  getCostAnalysis: async () => {
    return await callBackendApi('/api/azure/costs/summary')
  }
}

/**
 * Helper function to call backend API
 */
async function callBackendApi(endpoint) {
  try {
    const response = await fetch(`${BACKEND_API_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.portal.bearerToken}`
      }
    })

    if (!response.ok) {
      if (response.status === 404) {
        return {
          success: false,
          error: 'Backend API endpoint not available yet. This functionality is being implemented.'
        }
      }
      throw new Error(`API call failed: ${response.status}`)
    }

    const data = await response.json()
    return {
      success: true,
      data: data
    }
  } catch (error) {
    console.error('Azure API call error:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

/**
 * Get list of available Azure functions for the user
 */
export function getAvailableFunctions() {
  return [
    { id: 1, name: 'Get AKS Cluster Status', description: 'View the current status and health of the AKS cluster' },
    { id: 2, name: 'List HSPS Pods', description: 'List all pods running in the HSPS namespace' },
    { id: 3, name: 'List STAR Pods', description: 'List all pods running in the STAR namespace' },
    { id: 4, name: 'Get Pod Details', description: 'Get detailed information about a specific pod' },
    { id: 5, name: 'Get Resource Group Info', description: 'View information about the hsps-demo-rg resource group' },
    { id: 6, name: 'List All Resources', description: 'List all Azure resources in the resource group' },
    { id: 7, name: 'Get App Service Status', description: 'Check the status of the mckessondemo-csutherland App Service' },
    { id: 8, name: 'Get Function App Status', description: 'Check the status of the hsps-pod-shutdown Function App' },
    { id: 9, name: 'Get Storage Account Info', description: 'View storage account information and usage' },
    { id: 10, name: 'Get AKS Node Pools', description: 'View AKS node pool configuration and status' },
    { id: 11, name: 'Get Deployment Status', description: 'Check deployment status in a namespace' },
    { id: 12, name: 'Get Service Status', description: 'Check Kubernetes service status in a namespace' },
    { id: 13, name: 'Get Pod Logs', description: 'Retrieve the last 50 lines of logs from a pod' },
    { id: 14, name: 'Get Subscription Info', description: 'View Azure subscription information (non-sensitive)' },
    { id: 15, name: 'Get Cost Analysis', description: 'View cost summary for the last 30 days' }
  ]
}

/**
 * Detect which Azure function the user is asking about
 */
export function detectAzureFunction(userMessage) {
  const msg = userMessage.toLowerCase()

  // AKS Cluster Status
  if (msg.includes('aks') && (msg.includes('status') || msg.includes('health') || msg.includes('cluster'))) {
    return { function: 'getAksClusterStatus', params: [] }
  }

  // List Pods
  if (msg.includes('hsps') && (msg.includes('pod') || msg.includes('list'))) {
    return { function: 'listHspsPods', params: [] }
  }
  if (msg.includes('star') && (msg.includes('pod') || msg.includes('list'))) {
    return { function: 'listStarPods', params: [] }
  }

  // Pod Details
  if (msg.includes('pod') && msg.includes('detail')) {
    // Try to extract namespace and pod name
    return { function: 'getPodDetails', params: ['hsps', 'pod-name'] }
  }

  // Resource Group
  if (msg.includes('resource group') || msg.includes('resourcegroup')) {
    return { function: 'getResourceGroupInfo', params: [] }
  }

  // List Resources
  if (msg.includes('list') && msg.includes('resource')) {
    return { function: 'listAllResources', params: [] }
  }

  // App Service
  if (msg.includes('app service') || msg.includes('appservice') || msg.includes('web app')) {
    return { function: 'getAppServiceStatus', params: [] }
  }

  // Function App
  if (msg.includes('function app') || msg.includes('functionapp') || msg.includes('shutdown')) {
    return { function: 'getFunctionAppStatus', params: [] }
  }

  // Storage Account
  if (msg.includes('storage')) {
    return { function: 'getStorageAccountInfo', params: [] }
  }

  // Node Pools
  if (msg.includes('node') && (msg.includes('pool') || msg.includes('aks'))) {
    return { function: 'getAksNodePools', params: [] }
  }

  // Deployments
  if (msg.includes('deployment')) {
    const namespace = msg.includes('star') ? 'star' : 'hsps'
    return { function: 'getDeploymentStatus', params: [namespace] }
  }

  // Services
  if (msg.includes('service') && !msg.includes('app service')) {
    const namespace = msg.includes('star') ? 'star' : 'hsps'
    return { function: 'getServiceStatus', params: [namespace] }
  }

  // Pod Logs
  if (msg.includes('log')) {
    return { function: 'getPodLogs', params: ['hsps', 'pod-name'] }
  }

  // Subscription Info
  if (msg.includes('subscription')) {
    return { function: 'getSubscriptionInfo', params: [] }
  }

  // Cost Analysis
  if (msg.includes('cost') || msg.includes('spending') || msg.includes('bill')) {
    return { function: 'getCostAnalysis', params: [] }
  }

  // Available functions
  if (msg.includes('what can you do') || msg.includes('capabilities') || msg.includes('features')) {
    return { function: 'listCapabilities', params: [] }
  }

  return null
}
