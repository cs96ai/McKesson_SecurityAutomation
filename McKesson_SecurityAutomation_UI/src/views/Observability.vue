<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Observability & Monitoring</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Monitor automation health, metrics, and performance</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Error Budget</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ observabilityStore.metrics.errorBudget.current }}%</p>
        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Target: {{ observabilityStore.metrics.errorBudget.target }}%</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Active Alerts</p>
        <p class="text-3xl font-bold text-red-600 dark:text-red-400 mt-1">{{ activeAlertsCount }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Healthy Services</p>
        <p class="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">{{ healthyServicesCount }}/{{ observabilityStore.healthChecks.length }}</p>
      </div>
      <div class="card">
        <p class="text-sm text-gray-500 dark:text-gray-400">Avg Latency (P95)</p>
        <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ avgLatency }}ms</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Playbook Executions</h3>
        <Line :data="executionsChartData" :options="chartOptions" />
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Latency Percentiles</h3>
        <Line :data="latencyChartData" :options="chartOptions" />
      </div>
    </div>

    <div class="card">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Active Alerts</h3>
        <div class="flex space-x-2">
          <button @click="filterSeverity = 'All'" :class="filterSeverity === 'All' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">All</button>
          <button @click="filterSeverity = 'Critical'" :class="filterSeverity === 'Critical' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">Critical</button>
          <button @click="filterSeverity = 'Warning'" :class="filterSeverity === 'Warning' ? 'btn-primary' : 'btn-secondary'" class="text-sm py-1 px-3">Warning</button>
        </div>
      </div>

      <div class="space-y-3">
        <div
          v-for="alert in filteredAlerts"
          :key="alert.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
        >
          <div class="flex items-start justify-between mb-2">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-1">
                <span :class="[
                  'badge',
                  alert.severity === 'Critical' ? 'badge-danger' : alert.severity === 'Warning' ? 'badge-warning' : 'badge-info'
                ]">
                  {{ alert.severity }}
                </span>
                <h4 class="text-sm font-semibold text-gray-900 dark:text-white">{{ alert.title }}</h4>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-300">{{ alert.description }}</p>
              <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500 dark:text-gray-400">
                <span>{{ alert.affectedService }}</span>
                <span>•</span>
                <span>{{ formatDate(alert.timestamp) }}</span>
              </div>
            </div>
            <div class="flex space-x-2">
              <button
                v-if="alert.status === 'Active'"
                @click="acknowledgeAlert(alert.id)"
                class="text-xs btn-secondary py-1 px-3"
              >
                Acknowledge
              </button>
              <button
                @click="resolveAlert(alert.id)"
                class="text-xs btn-primary py-1 px-3"
              >
                Resolve
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Logs</h3>
          <select v-model="logLevelFilter" class="input-field text-sm">
            <option value="All">All Levels</option>
            <option value="ERROR">Error</option>
            <option value="WARN">Warning</option>
            <option value="INFO">Info</option>
          </select>
        </div>
        <div class="bg-gray-900 rounded-lg p-4 font-mono text-xs max-h-96 overflow-y-auto space-y-1">
          <div
            v-for="log in filteredLogs"
            :key="log.id"
            :class="[
              log.level === 'ERROR' ? 'text-red-400' : log.level === 'WARN' ? 'text-yellow-400' : 'text-gray-300'
            ]"
          >
            [{{ formatTime(log.timestamp) }}] [{{ log.level }}] [{{ log.service }}] {{ log.message }}
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Service Health</h3>
        <div class="space-y-3">
          <div
            v-for="service in observabilityStore.healthChecks"
            :key="service.service"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div :class="[
                'w-3 h-3 rounded-full',
                service.status === 'Healthy' ? 'bg-green-500' : service.status === 'Degraded' ? 'bg-yellow-500' : 'bg-red-500'
              ]"></div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">{{ service.service }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Uptime: {{ service.uptime }}</p>
              </div>
            </div>
            <span :class="[
              'badge',
              service.status === 'Healthy' ? 'badge-success' : service.status === 'Degraded' ? 'badge-warning' : 'badge-danger'
            ]">
              {{ service.status }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Distributed Traces</h3>
      <div class="space-y-4">
        <div
          v-for="trace in observabilityStore.traces"
          :key="trace.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
        >
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ trace.service }} - {{ trace.operation }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Trace ID: {{ trace.traceId }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ trace.duration }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(trace.timestamp) }}</p>
            </div>
          </div>

          <div class="space-y-2">
            <div v-for="(span, index) in trace.spans" :key="index" class="flex items-center space-x-2">
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs text-gray-600 dark:text-gray-400">{{ span.name }}</span>
                  <span class="text-xs text-gray-500 dark:text-gray-500">{{ span.duration }}</span>
                </div>
                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    class="bg-primary-600 h-2 rounded-full"
                    :style="{ width: `${(parseInt(span.duration) / parseInt(trace.duration.replace('s', '000'))) * 100}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { useObservabilityStore } from '@/stores/observability'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const observabilityStore = useObservabilityStore()

const filterSeverity = ref('All')
const logLevelFilter = ref('All')

const filteredAlerts = computed(() => {
  if (filterSeverity.value === 'All') {
    return observabilityStore.alerts
  }
  return observabilityStore.alerts.filter(a => a.severity === filterSeverity.value)
})

const filteredLogs = computed(() => {
  if (logLevelFilter.value === 'All') {
    return observabilityStore.logs
  }
  return observabilityStore.logs.filter(l => l.level === logLevelFilter.value)
})

const activeAlertsCount = computed(() => {
  return observabilityStore.alerts.filter(a => a.status === 'Active').length
})

const healthyServicesCount = computed(() => {
  return observabilityStore.healthChecks.filter(s => s.status === 'Healthy').length
})

const avgLatency = computed(() => {
  const latest = observabilityStore.metrics.latency[observabilityStore.metrics.latency.length - 1]
  return latest ? latest.p95 : 0
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: true
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const executionsChartData = computed(() => ({
  labels: observabilityStore.metrics.playbookExecutions.map(m => m.time),
  datasets: [
    {
      label: 'Success',
      data: observabilityStore.metrics.playbookExecutions.map(m => m.success),
      borderColor: 'rgb(34, 197, 94)',
      backgroundColor: 'rgba(34, 197, 94, 0.1)',
      tension: 0.4
    },
    {
      label: 'Failed',
      data: observabilityStore.metrics.playbookExecutions.map(m => m.failed),
      borderColor: 'rgb(239, 68, 68)',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4
    }
  ]
}))

const latencyChartData = computed(() => ({
  labels: observabilityStore.metrics.latency.map(m => m.time),
  datasets: [
    {
      label: 'P50',
      data: observabilityStore.metrics.latency.map(m => m.p50),
      borderColor: 'rgb(34, 197, 94)',
      backgroundColor: 'rgba(34, 197, 94, 0.1)',
      tension: 0.4
    },
    {
      label: 'P95',
      data: observabilityStore.metrics.latency.map(m => m.p95),
      borderColor: 'rgb(251, 191, 36)',
      backgroundColor: 'rgba(251, 191, 36, 0.1)',
      tension: 0.4
    },
    {
      label: 'P99',
      data: observabilityStore.metrics.latency.map(m => m.p99),
      borderColor: 'rgb(239, 68, 68)',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      tension: 0.4
    }
  ]
}))

function acknowledgeAlert(id) {
  observabilityStore.acknowledgeAlert(id)
}

function resolveAlert(id) {
  observabilityStore.resolveAlert(id)
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString()
}

function formatTime(dateString) {
  return new Date(dateString).toLocaleTimeString()
}
</script>
