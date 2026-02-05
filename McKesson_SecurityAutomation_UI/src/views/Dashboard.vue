<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Total Toil Reduction</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ automationStore.totalToilReduction }}%</p>
          </div>
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Active Automations</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ automationStore.activeAutomations }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Completed</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ automationStore.completedAutomations }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 dark:text-gray-400">Playbook Success Rate</p>
            <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">94%</p>
          </div>
          <div class="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Toil Reduction Over Time</h3>
        <Line :data="toilReductionChartData" :options="chartOptions" />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Playbook Success Rate</h3>
        <Line :data="successRateChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Platform Coverage</h3>
        <Bar :data="coverageChartData" :options="barChartOptions" />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Average Latency (ms)</h3>
        <Line :data="latencyChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quarterly Objectives</h3>
      <div class="space-y-4">
        <div v-for="objective in automationStore.objectives" :key="objective.id" class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div class="flex items-center justify-between mb-2">
            <div>
              <span class="text-xs font-medium text-gray-500 dark:text-gray-400">{{ objective.quarter }}</span>
              <h4 class="text-sm font-semibold text-gray-900 dark:text-white">{{ objective.title }}</h4>
            </div>
            <span :class="[
              'badge',
              objective.status === 'On Track' ? 'badge-success' : objective.status === 'At Risk' ? 'badge-warning' : 'badge-info'
            ]">
              {{ objective.status }}
            </span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="objective.status === 'On Track' ? 'bg-green-600' : objective.status === 'At Risk' ? 'bg-yellow-600' : 'bg-blue-600'"
              :style="{ width: `${objective.progress}%` }"
            ></div>
          </div>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ objective.progress }}% complete</p>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Automation Roadmap</h3>
        <div class="flex space-x-2">
          <button @click="filterStatus = 'All'" :class="filterStatus === 'All' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">All</button>
          <button @click="filterStatus = 'In Progress'" :class="filterStatus === 'In Progress' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">In Progress</button>
          <button @click="filterStatus = 'Completed'" :class="filterStatus === 'Completed' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">Completed</button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Use Case</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Priority</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Impact</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Quarter</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Owner</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="roadmap in filteredRoadmaps" :key="roadmap.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50">
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ roadmap.useCase }}</td>
              <td class="px-4 py-3 text-sm">
                <span :class="[
                  'badge',
                  roadmap.priority === 'High' ? 'badge-danger' : roadmap.priority === 'Medium' ? 'badge-warning' : 'badge-info'
                ]">
                  {{ roadmap.priority }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm">
                <span :class="[
                  'badge',
                  roadmap.status === 'Completed' ? 'badge-success' : roadmap.status === 'In Progress' ? 'badge-info' : 'badge-warning'
                ]">
                  {{ roadmap.status }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-900 dark:text-white">{{ roadmap.impact }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ roadmap.quarter }}</td>
              <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ roadmap.owner }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Line, Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { useAutomationStore } from '@/stores/automation'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

const automationStore = useAutomationStore()
const filterStatus = ref('All')

const filteredRoadmaps = computed(() => {
  if (filterStatus.value === 'All') {
    return automationStore.roadmaps
  }
  return automationStore.roadmaps.filter(r => r.status === filterStatus.value)
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const barChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  indexAxis: 'y',
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      max: 100
    }
  }
}

const toilReductionChartData = computed(() => ({
  labels: automationStore.metrics.toilReduction.map(m => m.month),
  datasets: [{
    label: 'Toil Reduction %',
    data: automationStore.metrics.toilReduction.map(m => m.value),
    borderColor: 'rgb(34, 197, 94)',
    backgroundColor: 'rgba(34, 197, 94, 0.1)',
    tension: 0.4,
    fill: true
  }]
}))

const successRateChartData = computed(() => ({
  labels: automationStore.metrics.playbookSuccess.map(m => m.month),
  datasets: [{
    label: 'Success Rate %',
    data: automationStore.metrics.playbookSuccess.map(m => m.value),
    borderColor: 'rgb(59, 130, 246)',
    backgroundColor: 'rgba(59, 130, 246, 0.1)',
    tension: 0.4,
    fill: true
  }]
}))

const latencyChartData = computed(() => ({
  labels: automationStore.metrics.latency.map(m => m.month),
  datasets: [{
    label: 'Latency (ms)',
    data: automationStore.metrics.latency.map(m => m.value),
    borderColor: 'rgb(168, 85, 247)',
    backgroundColor: 'rgba(168, 85, 247, 0.1)',
    tension: 0.4,
    fill: true
  }]
}))

const coverageChartData = computed(() => ({
  labels: Object.keys(automationStore.metrics.coverage),
  datasets: [{
    label: 'Coverage %',
    data: Object.values(automationStore.metrics.coverage),
    backgroundColor: [
      'rgba(59, 130, 246, 0.8)',
      'rgba(34, 197, 94, 0.8)',
      'rgba(168, 85, 247, 0.8)',
      'rgba(251, 191, 36, 0.8)',
      'rgba(239, 68, 68, 0.8)',
      'rgba(20, 184, 166, 0.8)'
    ]
  }]
}))
</script>
