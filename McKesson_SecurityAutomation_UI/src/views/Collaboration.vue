<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Collaboration Hub</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Technical leadership, mentoring, and team collaboration</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Team Tasks & Initiatives</h3>
          <div class="space-y-3">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
            >
              <div class="flex items-start justify-between mb-2">
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <input
                      type="checkbox"
                      :checked="task.completed"
                      @change="toggleTask(task.id)"
                      class="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                    />
                    <h4 :class="['text-sm font-semibold', task.completed ? 'line-through text-gray-500 dark:text-gray-500' : 'text-gray-900 dark:text-white']">
                      {{ task.title }}
                    </h4>
                  </div>
                  <p class="text-sm text-gray-600 dark:text-gray-300 ml-6">{{ task.description }}</p>
                </div>
                <span :class="[
                  'badge',
                  task.type === 'Operational' ? 'badge-info' : task.type === 'Resilience' ? 'badge-success' : 'badge-warning'
                ]">
                  {{ task.type }}
                </span>
              </div>
              <div class="flex items-center space-x-4 ml-6 mt-2 text-xs text-gray-500 dark:text-gray-400">
                <span>Team: {{ task.team }}</span>
                <span>•</span>
                <span>Due: {{ task.dueDate }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Knowledge Base</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="article in knowledgeBase"
              :key="article.id"
              class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200 cursor-pointer"
              @click="selectedArticle = article"
            >
              <div class="flex items-start space-x-3">
                <div :class="[
                  'w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0',
                  article.category === 'Python' ? 'bg-blue-100 dark:bg-blue-900/20' :
                  article.category === 'Integration' ? 'bg-green-100 dark:bg-green-900/20' :
                  article.category === 'Best Practices' ? 'bg-purple-100 dark:bg-purple-900/20' :
                  'bg-yellow-100 dark:bg-yellow-900/20'
                ]">
                  <svg class="w-6 h-6" :class="[
                    article.category === 'Python' ? 'text-blue-600 dark:text-blue-400' :
                    article.category === 'Integration' ? 'text-green-600 dark:text-green-400' :
                    article.category === 'Best Practices' ? 'text-purple-600 dark:text-purple-400' :
                    'text-yellow-600 dark:text-yellow-400'
                  ]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ article.title }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ article.category }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Team Metrics</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-3xl font-bold text-primary-600 dark:text-primary-400">24</p>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">Automations Delivered</p>
            </div>
            <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-3xl font-bold text-green-600 dark:text-green-400">95%</p>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">Team Satisfaction</p>
            </div>
            <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-3xl font-bold text-purple-600 dark:text-purple-400">8</p>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">Teams Supported</p>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Team Members</h3>
          <div class="space-y-3">
            <div
              v-for="member in teamMembers"
              :key="member.id"
              class="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <img :src="member.avatar" :alt="member.name" class="w-10 h-10 rounded-full" />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ member.name }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ member.role }}</p>
              </div>
              <div :class="[
                'w-2 h-2 rounded-full',
                member.status === 'online' ? 'bg-green-500' : 'bg-gray-400'
              ]"></div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Upcoming Events</h3>
          <div class="space-y-3">
            <div
              v-for="event in upcomingEvents"
              :key="event.id"
              class="border-l-4 border-primary-600 pl-3 py-2"
            >
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ event.title }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ event.date }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h3>
          <div class="space-y-2">
            <a href="#" class="block text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              → SOC Team Confluence
            </a>
            <a href="#" class="block text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              → Platform Ops Slack Channel
            </a>
            <a href="#" class="block text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              → IR Team Runbooks
            </a>
            <a href="#" class="block text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              → Automation GitHub Repo
            </a>
            <a href="#" class="block text-sm text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300">
              → Security Architecture Docs
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedArticle" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">{{ selectedArticle.title }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ selectedArticle.category }}</p>
            </div>
            <button @click="selectedArticle = null" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="prose dark:prose-invert max-w-none">
            <div v-html="selectedArticle.content"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const tasks = ref([
  { id: 1, title: 'Implement OAuth2 flow for new SIEM integration', description: 'Work with Platform Ops to establish secure authentication', type: 'Operational', team: 'Platform Ops', dueDate: '2026-02-10', completed: false },
  { id: 2, title: 'Design error handling patterns for playbooks', description: 'Create standardized error handling and retry logic', type: 'Resilience', team: 'SOC/IR', dueDate: '2026-02-08', completed: false },
  { id: 3, title: 'Conduct Python best practices workshop', description: 'Mentor team on async patterns and type hints', type: 'Operational', team: 'Security Team', dueDate: '2026-02-15', completed: false },
  { id: 4, title: 'Review compliance evidence collection automation', description: 'Ensure audit-ready evidence logs meet requirements', type: 'Compliance', team: 'Compliance', dueDate: '2026-02-12', completed: true },
  { id: 5, title: 'Optimize playbook execution latency', description: 'Reduce P95 latency below 400ms target', type: 'Resilience', team: 'Platform Team', dueDate: '2026-02-20', completed: false },
  { id: 6, title: 'Establish SLOs for automation platform', description: 'Define error budgets and reliability targets', type: 'Resilience', team: 'Platform Ops', dueDate: '2026-02-18', completed: false }
])

const knowledgeBase = ref([
  {
    id: 1,
    title: 'Python Async Patterns for Automation',
    category: 'Python',
    content: '<h4>Async/Await Best Practices</h4><p>Use asyncio for I/O-bound operations like API calls...</p><pre><code>async def fetch_threat_intel(ioc):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(f"https://api.threatintel.com/{ioc}") as resp:\n            return await resp.json()</code></pre>'
  },
  {
    id: 2,
    title: 'OAuth2 Integration Guide',
    category: 'Integration',
    content: '<h4>Implementing OAuth2 Flow</h4><p>Steps to implement OAuth2 authentication for API integrations...</p><ol><li>Register application with provider</li><li>Implement authorization code flow</li><li>Store tokens securely</li><li>Implement token refresh logic</li></ol>'
  },
  {
    id: 3,
    title: 'Event-Driven Architecture Patterns',
    category: 'Architecture',
    content: '<h4>Event-Driven Design</h4><p>Leverage message queues and event streams for scalable automation...</p><p>Use Kafka or RabbitMQ for asynchronous processing.</p>'
  },
  {
    id: 4,
    title: 'Error Handling & Retry Logic',
    category: 'Best Practices',
    content: '<h4>Resilient Error Handling</h4><p>Implement exponential backoff and circuit breaker patterns...</p><pre><code>@retry(stop=stop_after_attempt(3), wait=wait_exponential())\nasync def call_api(endpoint):\n    # API call logic\n    pass</code></pre>'
  },
  {
    id: 5,
    title: 'REST API Design Guidelines',
    category: 'Integration',
    content: '<h4>RESTful API Best Practices</h4><p>Follow REST principles for automation APIs...</p><ul><li>Use proper HTTP methods</li><li>Implement pagination</li><li>Version your APIs</li><li>Use proper status codes</li></ul>'
  },
  {
    id: 6,
    title: 'Terraform for Security Infrastructure',
    category: 'Infrastructure',
    content: '<h4>IaC with Terraform</h4><p>Manage security infrastructure as code...</p><pre><code>resource "aws_security_group" "automation" {\n  name = "automation-sg"\n  # Configuration...\n}</code></pre>'
  }
])

const teamMembers = ref([
  { id: 1, name: 'John Doe', role: 'Automation Lead', avatar: 'https://ui-avatars.com/api/?name=John+Doe&background=3b82f6&color=fff', status: 'online' },
  { id: 2, name: 'Jane Smith', role: 'SOC Analyst', avatar: 'https://ui-avatars.com/api/?name=Jane+Smith&background=10b981&color=fff', status: 'online' },
  { id: 3, name: 'Bob Wilson', role: 'Platform Engineer', avatar: 'https://ui-avatars.com/api/?name=Bob+Wilson&background=f59e0b&color=fff', status: 'offline' },
  { id: 4, name: 'Alice Brown', role: 'IR Specialist', avatar: 'https://ui-avatars.com/api/?name=Alice+Brown&background=8b5cf6&color=fff', status: 'online' },
  { id: 5, name: 'Charlie Davis', role: 'Security Engineer', avatar: 'https://ui-avatars.com/api/?name=Charlie+Davis&background=ef4444&color=fff', status: 'online' }
])

const upcomingEvents = ref([
  { id: 1, title: 'Automation Review Meeting', date: 'Feb 5, 2026 - 2:00 PM' },
  { id: 2, title: 'Python Workshop', date: 'Feb 7, 2026 - 10:00 AM' },
  { id: 3, title: 'SOC Team Sync', date: 'Feb 8, 2026 - 3:00 PM' },
  { id: 4, title: 'Platform Ops Standup', date: 'Feb 9, 2026 - 9:00 AM' }
])

const selectedArticle = ref(null)

function toggleTask(id) {
  const task = tasks.value.find(t => t.id === id)
  if (task) {
    task.completed = !task.completed
  }
}
</script>
