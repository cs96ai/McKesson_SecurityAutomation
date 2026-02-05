<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">API Integrations Hub</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage integrations between security tools and enterprise systems</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Total Integrations</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ integrationsStore.integrations.length }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Active</p>
        <p class="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">{{ activeCount }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Total API Calls Today</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ totalApiCalls.toLocaleString() }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Avg Error Rate</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ avgErrorRate.toFixed(2) }}%</p>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Integrations</h3>
        <div class="flex space-x-2">
          <select v-model="filterCategory" class="input-field text-sm">
            <option value="All">All Categories</option>
            <option value="SIEM/SOAR">SIEM/SOAR</option>
            <option value="Endpoint/EDR">Endpoint/EDR</option>
            <option value="Vulnerability Management">Vulnerability Management</option>
            <option value="Email Security">Email Security</option>
            <option value="Cloud Security">Cloud Security</option>
            <option value="Identity">Identity</option>
            <option value="ITSM">ITSM</option>
            <option value="ChatOps">ChatOps</option>
          </select>
          <select v-model="filterStatus" class="input-field text-sm">
            <option value="All">All Status</option>
            <option value="Active">Active</option>
            <option value="Maintenance">Maintenance</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div
          v-for="integration in filteredIntegrations"
          :key="integration.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200"
        >
          <div class="flex items-start justify-between mb-3">
            <div>
              <h4 class="text-lg font-semibold text-gray-900 dark:text-white">{{ integration.tool }}</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ integration.category }}</p>
            </div>
            <span :class="[
              'badge',
              integration.status === 'Active' ? 'badge-success' : integration.status === 'Maintenance' ? 'badge-warning' : 'badge-danger'
            ]">
              {{ integration.status }}
            </span>
          </div>

          <div class="space-y-2 mb-4">
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-300">
              <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Auth: {{ integration.authType }}
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-300">
              <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {{ integration.requestsPerDay.toLocaleString() }} requests/day
            </div>
            <div class="flex items-center text-sm text-gray-600 dark:text-gray-300">
              <svg class="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Error rate: {{ integration.errorRate }}%
            </div>
          </div>

          <div class="mb-3">
            <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">Integrated with:</p>
            <div class="flex flex-wrap gap-1">
              <span v-for="(tool, index) in integration.integratedWith" :key="index" class="badge badge-info text-xs">
                {{ tool }}
              </span>
            </div>
          </div>

          <div class="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
            <span class="text-xs text-gray-500 dark:text-gray-400">
              Last sync: {{ formatDate(integration.lastSync) }}
            </span>
            <button
              @click="testIntegration(integration.id)"
              :disabled="testing === integration.id"
              class="text-xs btn-primary py-1 px-3"
            >
              {{ testing === integration.id ? 'Testing...' : 'Test' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent API Logs</h3>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Integration</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Method</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Endpoint</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Duration</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Timestamp</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Error</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="log in integrationsStore.apiLogs" :key="log.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">{{ log.integration }}</td>
              <td class="px-4 py-3 text-sm">
                <span :class="[
                  'badge',
                  log.method === 'GET' ? 'badge-info' : log.method === 'POST' ? 'badge-success' : 'badge-warning'
                ]">
                  {{ log.method }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-600 dark:text-gray-300 font-mono">{{ log.endpoint }}</td>
              <td class="px-4 py-3 text-sm">
                <span :class="[
                  'badge',
                  log.status >= 200 && log.status < 300 ? 'badge-success' : 'badge-danger'
                ]">
                  {{ log.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ log.duration }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ formatDate(log.timestamp) }}</td>
              <td class="px-4 py-3 text-sm text-red-600 dark:text-red-400">{{ log.error || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Integration Architecture</h3>
      <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-6">
        <div class="flex flex-wrap justify-center gap-8">
          <div class="text-center">
            <div class="w-24 h-24 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-12 h-12 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">SIEM/SOAR</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Core Platform</p>
          </div>

          <div class="flex items-center">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </div>

          <div class="text-center">
            <div class="w-24 h-24 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-12 h-12 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">Endpoints</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">EDR Systems</p>
          </div>

          <div class="flex items-center">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </div>

          <div class="text-center">
            <div class="w-24 h-24 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-12 h-12 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
              </svg>
            </div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">Cloud</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">AWS/Azure/GCP</p>
          </div>

          <div class="flex items-center">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
          </div>

          <div class="text-center">
            <div class="w-24 h-24 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center justify-center mb-2">
              <svg class="w-12 h-12 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <p class="text-sm font-medium text-gray-900 dark:text-white">ITSM</p>
            <p class="text-xs text-gray-500 dark:text-gray-400">ServiceNow</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useIntegrationsStore } from '@/stores/integrations'
import { useToast } from 'vue-toastification'

const integrationsStore = useIntegrationsStore()
const toast = useToast()

const filterCategory = ref('All')
const filterStatus = ref('All')
const testing = ref(null)

const filteredIntegrations = computed(() => {
  let filtered = integrationsStore.integrations

  if (filterCategory.value !== 'All') {
    filtered = filtered.filter(i => i.category === filterCategory.value)
  }

  if (filterStatus.value !== 'All') {
    filtered = filtered.filter(i => i.status === filterStatus.value)
  }

  return filtered
})

const activeCount = computed(() => {
  return integrationsStore.integrations.filter(i => i.status === 'Active').length
})

const totalApiCalls = computed(() => {
  return integrationsStore.integrations.reduce((sum, i) => sum + i.requestsPerDay, 0)
})

const avgErrorRate = computed(() => {
  const total = integrationsStore.integrations.reduce((sum, i) => sum + i.errorRate, 0)
  return total / integrationsStore.integrations.length
})

async function testIntegration(id) {
  testing.value = id
  try {
    const result = await integrationsStore.testIntegration(id)
    if (result.success) {
      toast.success('Integration test successful')
    } else {
      toast.error('Integration test failed')
    }
  } catch (error) {
    toast.error('Failed to test integration')
  } finally {
    testing.value = null
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}
</script>
