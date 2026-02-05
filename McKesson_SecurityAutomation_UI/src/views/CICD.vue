<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">CI/CD Workflows</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage automation deployment pipelines</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Total Pipelines</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ cicdStore.pipelines.length }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Running</p>
        <p class="text-3xl font-bold text-blue-600 dark:text-blue-400 mt-1">{{ runningCount }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Success Rate</p>
        <p class="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">{{ successRate }}%</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Active Deployments</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ activeDeployments }}</p>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Pipelines</h3>
        <div class="flex space-x-2">
          <select v-model="filterEnvironment" class="input-field text-sm">
            <option value="All">All Environments</option>
            <option value="Production">Production</option>
            <option value="Development">Development</option>
            <option value="CI">CI</option>
          </select>
        </div>
      </div>

      <div class="space-y-4">
        <div
          v-for="pipeline in filteredPipelines"
          :key="pipeline.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center space-x-3">
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white">{{ pipeline.name }}</h4>
                <span :class="[
                  'badge',
                  pipeline.status === 'Success' ? 'badge-success' : pipeline.status === 'Running' ? 'badge-info' : 'badge-danger'
                ]">
                  {{ pipeline.status }}
                </span>
              </div>
              <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                <span>{{ pipeline.repository }} / {{ pipeline.branch }}</span>
                <span>•</span>
                <span>{{ pipeline.environment }}</span>
                <span>•</span>
                <span>{{ pipeline.duration }}</span>
              </div>
            </div>
            <button
              @click="runPipeline(pipeline.id)"
              :disabled="running === pipeline.id || pipeline.status === 'Running'"
              class="btn-primary text-sm"
            >
              {{ running === pipeline.id ? 'Starting...' : 'Run Pipeline' }}
            </button>
          </div>

          <div class="flex items-center space-x-2 mb-3">
            <div
              v-for="(stage, index) in pipeline.stages"
              :key="index"
              class="flex-1"
            >
              <div class="flex items-center">
                <div
                  :class="[
                    'flex-1 h-2 rounded-full',
                    pipeline.status === 'Success' ? 'bg-green-500' :
                    pipeline.status === 'Running' && index <= 2 ? 'bg-blue-500' :
                    pipeline.status === 'Failed' && index <= 2 ? 'bg-red-500' :
                    'bg-gray-300 dark:bg-gray-600'
                  ]"
                ></div>
                <div v-if="index < pipeline.stages.length - 1" class="w-2"></div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ stage }}</p>
            </div>
          </div>

          <div class="flex items-center justify-between text-sm">
            <div class="flex items-center space-x-4 text-gray-500 dark:text-gray-400">
              <span>Triggered by: {{ pipeline.triggeredBy }}</span>
              <span>•</span>
              <span>{{ formatDate(pipeline.lastRun) }}</span>
            </div>
            <div v-if="pipeline.error" class="text-red-600 dark:text-red-400">
              {{ pipeline.error }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Deployments</h3>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Pipeline</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Environment</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Version</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="deployment in cicdStore.deployments" :key="deployment.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ deployment.pipeline }}</td>
                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ deployment.environment }}</td>
                <td class="px-4 py-3 text-sm font-mono text-gray-900 dark:text-white">{{ deployment.version }}</td>
                <td class="px-4 py-3 text-sm">
                  <span :class="[
                    'badge',
                    deployment.status === 'Active' ? 'badge-success' : 'badge-danger'
                  ]">
                    {{ deployment.status }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm">
                  <button
                    v-if="deployment.status === 'Active'"
                    @click="rollback(deployment.id)"
                    :disabled="rollingBack === deployment.id"
                    class="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 text-xs"
                  >
                    {{ rollingBack === deployment.id ? 'Rolling back...' : 'Rollback' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Secrets Management</h3>
        <div class="space-y-3">
          <div
            v-for="secret in cicdStore.secrets"
            :key="secret.id"
            class="border border-gray-200 dark:border-gray-700 rounded-lg p-3"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-900 dark:text-white">{{ secret.name }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ secret.scope }}</p>
              </div>
              <span :class="[
                'badge',
                secret.status === 'Active' ? 'badge-success' : 'badge-warning'
              ]">
                {{ secret.status }}
              </span>
            </div>
            <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
              <span>Expires in {{ secret.expiresIn }}</span>
              <button
                @click="rotateSecret(secret.id)"
                :disabled="rotating === secret.id"
                class="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300"
              >
                {{ rotating === secret.id ? 'Rotating...' : 'Rotate' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Pipeline Configuration Example</h3>
      <div class="bg-gray-900 rounded-lg p-4 font-mono text-sm text-gray-300 overflow-x-auto">
        <pre v-pre>name: Automation Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Security scan
        run: |
          bandit -r src/
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          ./deploy.sh production
        env:
          API_KEY: ${{ secrets.API_KEY }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCICDStore } from '@/stores/cicd'
import { useToast } from 'vue-toastification'

const cicdStore = useCICDStore()
const toast = useToast()

const filterEnvironment = ref('All')
const running = ref(null)
const rollingBack = ref(null)
const rotating = ref(null)

const filteredPipelines = computed(() => {
  if (filterEnvironment.value === 'All') {
    return cicdStore.pipelines
  }
  return cicdStore.pipelines.filter(p => p.environment === filterEnvironment.value)
})

const runningCount = computed(() => {
  return cicdStore.pipelines.filter(p => p.status === 'Running').length
})

const successRate = computed(() => {
  const total = cicdStore.pipelines.length
  const successful = cicdStore.pipelines.filter(p => p.status === 'Success').length
  return Math.round((successful / total) * 100)
})

const activeDeployments = computed(() => {
  return cicdStore.deployments.filter(d => d.status === 'Active').length
})

async function runPipeline(id) {
  running.value = id
  try {
    const result = await cicdStore.runPipeline(id)
    if (result.status === 'Success') {
      toast.success('Pipeline completed successfully')
    } else {
      toast.error('Pipeline failed: ' + (result.error || 'Unknown error'))
    }
  } catch (error) {
    toast.error('Failed to run pipeline')
  } finally {
    running.value = null
  }
}

async function rollback(id) {
  rollingBack.value = id
  try {
    await cicdStore.rollbackDeployment(id)
    toast.success('Deployment rolled back successfully')
  } catch (error) {
    toast.error('Failed to rollback deployment')
  } finally {
    rollingBack.value = null
  }
}

async function rotateSecret(id) {
  rotating.value = id
  try {
    await cicdStore.rotateSecret(id)
    toast.success('Secret rotated successfully')
  } catch (error) {
    toast.error('Failed to rotate secret')
  } finally {
    rotating.value = null
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}
</script>
