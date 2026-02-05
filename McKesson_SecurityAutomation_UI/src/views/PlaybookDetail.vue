<template>
  <div v-if="playbook" class="space-y-6">
    <div class="flex items-center space-x-4">
      <button @click="$router.back()" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      </button>
      <div class="flex-1">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ playbook.name }}</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ playbook.category }}</p>
      </div>
      <span :class="[
        'badge',
        playbook.status === 'Active' ? 'badge-success' : playbook.status === 'Testing' ? 'badge-warning' : 'badge-danger'
      ]">
        {{ playbook.status }}
      </span>
      <button @click="executePlaybook" :disabled="executing" class="btn-primary">
        {{ executing ? 'Executing...' : 'Execute Playbook' }}
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Success Rate</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ playbook.successRate }}%</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Avg Execution Time</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ playbook.avgExecutionTime }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Version</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ playbook.version }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Owner</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ playbook.owner }}</p>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Description</h3>
      <p class="text-gray-600 dark:text-gray-300">{{ playbook.description }}</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Triggers</h3>
        <div class="space-y-2">
          <div v-for="(trigger, index) in playbook.triggers" :key="index" class="flex items-center space-x-2">
            <svg class="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span class="text-sm text-gray-700 dark:text-gray-300">{{ trigger }}</span>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Execution Steps</h3>
        <ol class="space-y-2">
          <li v-for="(step, index) in playbook.steps" :key="index" class="flex items-start space-x-3">
            <span class="flex-shrink-0 w-6 h-6 bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-full flex items-center justify-center text-xs font-medium">
              {{ index + 1 }}
            </span>
            <span class="text-sm text-gray-700 dark:text-gray-300 pt-0.5">{{ step }}</span>
          </li>
        </ol>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Executions</h3>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Start Time</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Duration</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Triggered By</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Error</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="execution in recentExecutions" :key="execution.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="px-4 py-3 text-sm">
                <span :class="[
                  'badge',
                  execution.status === 'Success' ? 'badge-success' : 'badge-danger'
                ]">
                  {{ execution.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ formatDate(execution.startTime) }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ execution.duration }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ execution.triggeredBy }}</td>
              <td class="px-4 py-3 text-sm text-red-600 dark:text-red-400">{{ execution.error || '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Simulated Output</h3>
      <div class="bg-gray-900 rounded-lg p-4 font-mono text-sm text-green-400 overflow-x-auto">
        <div v-if="executing">
          <p>Starting playbook execution...</p>
          <p class="mt-2">Loading configuration...</p>
          <p class="mt-1">Initializing connections...</p>
          <p class="mt-1 text-yellow-400">Executing steps...</p>
        </div>
        <div v-else-if="lastExecution">
          <p>[{{ formatDate(lastExecution.startTime) }}] Playbook: {{ playbook.name }}</p>
          <p class="mt-2">[INFO] Starting execution...</p>
          <p v-for="(step, index) in playbook.steps" :key="index" class="mt-1">
            [INFO] Step {{ index + 1 }}: {{ step }} - {{ lastExecution.status === 'Success' ? 'COMPLETED' : (index === 2 ? 'FAILED' : 'COMPLETED') }}
          </p>
          <p class="mt-2" :class="lastExecution.status === 'Success' ? 'text-green-400' : 'text-red-400'">
            [{{ lastExecution.status === 'Success' ? 'SUCCESS' : 'ERROR' }}] Execution {{ lastExecution.status === 'Success' ? 'completed' : 'failed' }} in {{ lastExecution.duration }}
          </p>
          <p v-if="lastExecution.error" class="mt-1 text-red-400">[ERROR] {{ lastExecution.error }}</p>
        </div>
        <div v-else>
          <p class="text-gray-500">No recent execution output available. Click "Execute Playbook" to run.</p>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="card">
    <p class="text-center text-gray-500 dark:text-gray-400">Playbook not found</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePlaybooksStore } from '@/stores/playbooks'
import { useToast } from 'vue-toastification'

const route = useRoute()
const playbooksStore = usePlaybooksStore()
const toast = useToast()

const executing = ref(false)
const playbook = ref(null)

const recentExecutions = computed(() => {
  return playbooksStore.executions.filter(e => e.playbookId === playbook.value?.id).slice(0, 10)
})

const lastExecution = computed(() => {
  return recentExecutions.value[0] || null
})

onMounted(() => {
  playbook.value = playbooksStore.getPlaybookById(route.params.id)
})

async function executePlaybook() {
  executing.value = true
  try {
    const result = await playbooksStore.executePlaybook(playbook.value.id)
    if (result.status === 'Success') {
      toast.success('Playbook executed successfully')
    } else {
      toast.error('Playbook execution failed: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    toast.error('Failed to execute playbook')
  } finally {
    executing.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}
</script>
