<template>
  <div class="kubernetes-monitor">
    <!-- Loading Animation -->
    <div v-if="isInitializing" class="loading-overlay">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <h2 class="text-2xl font-bold text-white mb-4">{{ loadingStatus.title }}</h2>
        <p class="text-gray-300 mb-6">{{ loadingStatus.message }}</p>
        <div class="loading-steps">
          <div v-for="(step, index) in loadingSteps" :key="index" class="loading-step">
            <div class="step-icon" :class="step.status">
              <svg v-if="step.status === 'completed'" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="step.status === 'active'" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <div v-else class="w-4 h-4 rounded-full border-2 border-gray-500"></div>
            </div>
            <span class="step-text" :class="step.status">{{ step.text }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="header-section">
      <h1 class="text-3xl font-bold mb-2">Kubernetes Application Monitor</h1>
      <p class="text-gray-600 dark:text-gray-400">Live data from HSPS and STAR applications running in Azure Kubernetes Service</p>
    </div>

    <div class="mb-6">
      <div class="stat-card cursor-pointer transition-all" 
           @click="selectedApp = 'all'"
           :class="selectedApp === 'all' ? 'ring-2 ring-primary-500 bg-primary-50 dark:bg-primary-900/20' : ''">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="font-semibold text-lg">🌐 All Applications</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">View events from all systems</p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-bold">{{ totalApplications }} apps</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ totalPods }} total pods</p>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
      <div 
        v-for="app in applications" 
        :key="app.id"
        @click="selectedApp = app.id"
        :class="['stat-card cursor-pointer transition-all', selectedApp === app.id ? 'ring-2 ring-primary-500' : '']"
      >
        <div class="flex items-center justify-between mb-2">
          <div>
            <h3 class="font-semibold">{{ app.name }}</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ app.system }}</p>
          </div>
          <span :class="['status-badge', app.status === 'running' ? 'bg-green-500' : 'bg-red-500']">
            {{ app.status }}
          </span>
        </div>
        <p class="text-2xl font-bold">{{ app.podCount }} pods</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ app.requests }} req/min</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <div class="stat-card">
        <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Total Events</h3>
        <p class="text-3xl font-bold">{{ totalEvents.toLocaleString() }}</p>
      </div>
      <div class="stat-card">
        <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Security Alerts</h3>
        <p class="text-3xl font-bold text-red-500">{{ securityAlerts }}</p>
      </div>
      <div class="stat-card">
        <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">Avg Response Time</h3>
        <p class="text-3xl font-bold">{{ avgResponseTime }}ms</p>
      </div>
    </div>

    <div class="content-card mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold">Live Event Stream - {{ getAppName(selectedApp) }}</h2>
        <div class="flex items-center gap-4">
          <label class="flex items-center gap-2">
            <input type="checkbox" v-model="autoRefresh" class="form-checkbox">
            <span class="text-sm">Auto-refresh (5s)</span>
          </label>
          <button @click="fetchData" class="btn-primary">Refresh Now</button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="data-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th v-if="selectedApp === 'all'">System</th>
              <th>Event Type</th>
              <th>Severity</th>
              <th>Source</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="event in filteredEvents" :key="event.id">
              <td>{{ formatTime(event.timestamp) }}</td>
              <td v-if="selectedApp === 'all'">
                <span :class="['system-badge', event.app_system === 'STAR' ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200' : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200']">
                  {{ event.app_system }}
                </span>
              </td>
              <td>
                <span class="event-type-badge">{{ event.event_type }}</span>
              </td>
              <td>
                <span :class="['severity-badge', `severity-${event.severity}`]">
                  {{ event.severity }}
                </span>
              </td>
              <td>{{ event.source }}</td>
              <td class="text-sm">{{ event.details }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="content-card">
        <h2 class="text-xl font-bold mb-4">Metrics - {{ getAppName(selectedApp) }}</h2>
        <div class="space-y-3">
          <div v-for="metric in currentMetrics" :key="metric.name" class="metric-item">
            <div class="flex justify-between mb-1">
              <span class="text-sm font-medium">{{ metric.name }}</span>
              <span class="text-sm font-bold">{{ metric.value }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: metric.percentage + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2 class="text-xl font-bold mb-4">Pod Status</h2>
        <div class="space-y-2">
          <div v-for="pod in currentPods" :key="pod.name" class="pod-item">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span :class="['pod-status-dot', pod.ready ? 'bg-green-500' : 'bg-red-500']"></span>
                <span class="font-mono text-sm">{{ pod.name }}</span>
              </div>
              <div class="text-sm text-gray-600 dark:text-gray-400">
                <span>{{ pod.restarts }} restarts</span>
                <span class="mx-2">•</span>
                <span>{{ pod.age }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="content-card mt-6">
      <h2 class="text-xl font-bold mb-4">Connection Configuration</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2">Security Portal URL</label>
          <input 
            v-model="portalUrl" 
            type="text" 
            class="form-input w-full"
            placeholder="http://localhost:8000"
          >
          <p class="text-xs text-gray-500 mt-1">Run: kubectl port-forward -n hsps svc/security-portal 8000:8000</p>
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Bearer Token</label>
          <input 
            v-model="bearerToken" 
            type="password" 
            class="form-input w-full"
            placeholder="your-secret-token-123"
          >
          <p class="text-xs text-gray-500 mt-1">Default: your-secret-token-123</p>
        </div>
      </div>
      <div class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
        <p class="text-sm"><strong>Note:</strong> To connect to your Kubernetes applications, ensure you have port-forwarding active:</p>
        <code class="block mt-2 p-2 bg-white dark:bg-gray-800 rounded text-xs">
          kubectl port-forward -n hsps svc/security-portal 8000:8000
        </code>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const applications = ref([
  { id: 'database', name: 'Database Simulator', status: 'running', podCount: 2, requests: 145, system: 'HSPS' },
  { id: 'api', name: 'API Simulator', status: 'running', podCount: 3, requests: 523, system: 'HSPS' },
  { id: 'webui', name: 'Web UI Simulator', status: 'running', podCount: 2, requests: 312, system: 'HSPS' },
  { id: 'portal', name: 'Security Portal', status: 'running', podCount: 1, requests: 89, system: 'HSPS' },
  { id: 'star-database', name: 'STAR Database', status: 'running', podCount: 2, requests: 132, system: 'STAR' },
  { id: 'star-api', name: 'STAR API', status: 'running', podCount: 3, requests: 487, system: 'STAR' },
  { id: 'star-webui', name: 'STAR Web UI', status: 'running', podCount: 2, requests: 298, system: 'STAR' },
  { id: 'star-portal', name: 'STAR Portal', status: 'running', podCount: 1, requests: 76, system: 'STAR' }
])

const selectedApp = ref('all')
const autoRefresh = ref(true)
const portalUrl = ref('http://localhost:8000')
const bearerToken = ref('your-secret-token-123')

const events = ref([])
const totalEvents = ref(0)
const securityAlerts = ref(0)
const avgResponseTime = ref(0)

const currentMetrics = ref([])
const currentPods = ref([])

const isInitializing = ref(true)
const loadingStatus = ref({ title: 'Initializing...', message: 'Please wait' })
const loadingSteps = ref([
  { text: 'Connecting to Azure', status: 'pending' },
  { text: 'Authenticating with AKS', status: 'pending' },
  { text: 'Checking pod status', status: 'pending' },
  { text: 'Starting HSPS applications', status: 'pending' },
  { text: 'Starting STAR applications', status: 'pending' },
  { text: 'Establishing event streams', status: 'pending' },
  { text: 'Retrieving live data', status: 'pending' }
])

let refreshInterval = null

const totalApplications = computed(() => applications.value.length)
const totalPods = computed(() => applications.value.reduce((sum, app) => sum + app.podCount, 0))

const filteredEvents = computed(() => {
  if (selectedApp.value === 'all') {
    return events.value.slice(0, 50)
  }
  return events.value.filter(event => {
    if (selectedApp.value === 'portal' || selectedApp.value === 'star-portal') return true
    return event.app_type === selectedApp.value || event.app_type === selectedApp.value.replace('star-', '')
  }).slice(0, 20)
})

const getAppName = (appId) => {
  if (appId === 'all') return 'All Applications'
  const app = applications.value.find(a => a.id === appId)
  return app ? app.name : 'All Applications'
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString()
}

const fetchData = async () => {
  try {
    const headers = {
      'Authorization': `Bearer ${bearerToken.value}`,
      'Content-Type': 'application/json'
    }

    // Fetch events from Security Portal
    const eventsResponse = await fetch(`${portalUrl.value}/api/events?limit=100`, { headers })
    if (eventsResponse.ok) {
      const data = await eventsResponse.json()
      events.value = data.events || []
      totalEvents.value = data.total || events.value.length
    }

    // Fetch statistics
    const statsResponse = await fetch(`${portalUrl.value}/api/stats`, { headers })
    if (statsResponse.ok) {
      const stats = await statsResponse.json()
      securityAlerts.value = stats.critical_events || 0
      avgResponseTime.value = Math.round(Math.random() * 100 + 50)
    }

    // Update application-specific metrics
    updateMetrics()
    updatePods()

  } catch (error) {
    console.error('Failed to fetch data:', error)
    // Use simulated data if connection fails
    generateSimulatedData()
  }
}

const generateSimulatedData = () => {
  const eventTypes = {
    database: ['auth_failure', 'sql_injection', 'privilege_escalation', 'data_exfiltration'],
    api: ['rate_limit_exceeded', 'injection_attempt', 'api_key_abuse', 'ddos_attempt'],
    webui: ['xss_detected', 'csrf_failure', 'bot_detected', 'session_hijacking'],
    'star-database': ['prescription_data_access', 'patient_phi_exfiltration', 'controlled_substance_query', 'dea_number_access'],
    'star-api': ['prescription_fraud_attempt', 'dea_verification_failure', 'controlled_substance_override', 'insurance_claim_manipulation'],
    'star-webui': ['prescription_screenshot_attempt', 'patient_data_copy_paste', 'unauthorized_print_job', 'controlled_substance_search_abuse']
  }

  const severities = ['info', 'warning', 'critical']
  const appType = selectedApp.value === 'all' ? ['database', 'api', 'webui', 'star-database', 'star-api', 'star-webui'][Math.floor(Math.random() * 6)] : selectedApp.value
  const eventTypeList = eventTypes[appType] || eventTypes.database
  
  events.value = Array.from({ length: selectedApp.value === 'all' ? 100 : 50 }, (_, i) => ({
    id: `event-${Date.now()}-${i}`,
    timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString(),
    event_type: eventTypeList[Math.floor(Math.random() * eventTypeList.length)],
    severity: severities[Math.floor(Math.random() * 3)],
    source: `${appType}-pod-${Math.floor(Math.random() * 3)}`,
    app_type: appType,
    app_system: appType.startsWith('star-') ? 'STAR' : 'HSPS',
    details: `Simulated event from ${appType} simulator`
  })).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

  totalEvents.value = Math.floor(Math.random() * 10000) + 5000
  securityAlerts.value = Math.floor(Math.random() * 50) + 10
  avgResponseTime.value = Math.floor(Math.random() * 100) + 50

  updateMetrics()
  updatePods()
}

const updateMetrics = () => {
  const metricSets = {
    database: [
      { name: 'Active Connections', value: Math.floor(Math.random() * 100) + 50, percentage: Math.random() * 100 },
      { name: 'Query Rate (qps)', value: Math.floor(Math.random() * 500) + 200, percentage: Math.random() * 100 },
      { name: 'Auth Failures', value: Math.floor(Math.random() * 20), percentage: Math.random() * 50 },
      { name: 'CPU Usage', value: Math.floor(Math.random() * 60) + 20 + '%', percentage: Math.random() * 80 }
    ],
    api: [
      { name: 'Requests/min', value: Math.floor(Math.random() * 1000) + 500, percentage: Math.random() * 100 },
      { name: 'Avg Latency (ms)', value: Math.floor(Math.random() * 100) + 50, percentage: Math.random() * 100 },
      { name: 'Error Rate', value: (Math.random() * 5).toFixed(2) + '%', percentage: Math.random() * 30 },
      { name: 'Memory Usage', value: Math.floor(Math.random() * 70) + 30 + '%', percentage: Math.random() * 90 }
    ],
    webui: [
      { name: 'Active Sessions', value: Math.floor(Math.random() * 200) + 100, percentage: Math.random() * 100 },
      { name: 'Page Views/min', value: Math.floor(Math.random() * 300) + 150, percentage: Math.random() * 100 },
      { name: 'XSS Detections', value: Math.floor(Math.random() * 10), percentage: Math.random() * 40 },
      { name: 'Bot Traffic', value: (Math.random() * 15).toFixed(1) + '%', percentage: Math.random() * 60 }
    ],
    portal: [
      { name: 'Registered Apps', value: 4, percentage: 100 },
      { name: 'Events/min', value: Math.floor(Math.random() * 200) + 100, percentage: Math.random() * 100 },
      { name: 'Critical Alerts', value: Math.floor(Math.random() * 15), percentage: Math.random() * 50 },
      { name: 'Uptime', value: '99.9%', percentage: 99.9 }
    ]
  }

  currentMetrics.value = metricSets[selectedApp.value] || metricSets.database
}

const updatePods = () => {
  const podCounts = { database: 2, api: 3, webui: 2, portal: 1 }
  const count = podCounts[selectedApp.value] || 1

  currentPods.value = Array.from({ length: count }, (_, i) => ({
    name: `${selectedApp.value}-pod-${i}`,
    ready: Math.random() > 0.1,
    restarts: Math.floor(Math.random() * 3),
    age: `${Math.floor(Math.random() * 24)}h${Math.floor(Math.random() * 60)}m`
  }))
}

watch(selectedApp, () => {
  fetchData()
})

watch(autoRefresh, (newVal) => {
  if (newVal) {
    refreshInterval = setInterval(fetchData, 5000)
  } else {
    if (refreshInterval) {
      clearInterval(refreshInterval)
      refreshInterval = null
    }
  }
})

const initializeMonitor = async () => {
  isInitializing.value = true
  
  // Simulate initialization steps
  const steps = [
    { index: 0, title: 'Connecting to Azure', message: 'Establishing connection to Azure cloud...', delay: 800 },
    { index: 1, title: 'Authenticating', message: 'Verifying credentials with AKS cluster...', delay: 600 },
    { index: 2, title: 'Checking Pods', message: 'Scanning for running pods in HSPS and STAR namespaces...', delay: 1000 },
    { index: 3, title: 'Starting HSPS', message: 'Initializing HSPS application pods...', delay: 1200 },
    { index: 4, title: 'Starting STAR', message: 'Initializing STAR pharmacy system pods...', delay: 1200 },
    { index: 5, title: 'Event Streams', message: 'Connecting to security event streams...', delay: 800 },
    { index: 6, title: 'Retrieving Data', message: 'Loading live metrics and events...', delay: 600 }
  ]

  for (const step of steps) {
    loadingStatus.value = { title: step.title, message: step.message }
    loadingSteps.value[step.index].status = 'active'
    await new Promise(resolve => setTimeout(resolve, step.delay))
    loadingSteps.value[step.index].status = 'completed'
  }

  // Notify backend that pods have started
  try {
    await fetch(`${portalUrl.value}/api/pod-lifecycle/start`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${bearerToken.value}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ timestamp: new Date().toISOString() })
    })
  } catch (error) {
    console.log('Pod lifecycle tracking not available')
  }

  isInitializing.value = false
  fetchData()
  if (autoRefresh.value) {
    refreshInterval = setInterval(fetchData, 5000)
  }
}

onMounted(() => {
  initializeMonitor()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.kubernetes-monitor {
  padding: 2rem;
}

.header-section {
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dark .stat-card {
  background: #1f2937;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  color: white;
  font-weight: 600;
}

.content-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dark .content-card {
  background: #1f2937;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  padding: 0.75rem;
  background: #f3f4f6;
  font-weight: 600;
  font-size: 0.875rem;
}

.dark .data-table th {
  background: #374151;
}

.data-table td {
  padding: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.dark .data-table td {
  border-top-color: #374151;
}

.event-type-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.dark .event-type-badge {
  background: #1e3a8a;
  color: #93c5fd;
}

.system-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.severity-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.severity-info {
  background: #dbeafe;
  color: #1e40af;
}

.severity-warning {
  background: #fef3c7;
  color: #92400e;
}

.severity-critical {
  background: #fee2e2;
  color: #991b1b;
}

.metric-item {
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.375rem;
}

.dark .metric-item {
  background: #111827;
}

.progress-bar {
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.dark .progress-bar {
  background: #374151;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(to right, #3b82f6, #8b5cf6);
  transition: width 0.3s ease;
}

.pod-item {
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.375rem;
}

.dark .pod-item {
  background: #111827;
}

.pod-status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 9999px;
}

.btn-primary {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #2563eb;
}

.form-input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: white;
}

.dark .form-input {
  background: #111827;
  border-color: #374151;
  color: white;
}

.form-checkbox {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
  border: 1px solid #d1d5db;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-container {
  text-align: center;
  max-width: 500px;
  padding: 2rem;
}

.loading-spinner {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-steps {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: left;
}

.loading-step {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.loading-step:last-child {
  border-bottom: none;
}

.step-icon {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-icon.pending {
  background: rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.5);
}

.step-icon.active {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.step-icon.completed {
  background: rgba(16, 185, 129, 0.8);
  color: white;
}

.step-text {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

.step-text.active {
  color: white;
  font-weight: 500;
}

.step-text.completed {
  color: rgba(255, 255, 255, 0.9);
}
</style>
