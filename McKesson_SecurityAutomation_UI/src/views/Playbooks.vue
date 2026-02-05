<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Playbooks & Scripts</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage automation playbooks and scripts</p>
      </div>
      <button @click="showCreateModal = true" class="btn-primary">
        <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Create Playbook
      </button>
    </div>

    <div class="card">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 mb-6">
        <div class="flex-1 max-w-md">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search playbooks..."
            class="input-field"
          />
        </div>
        <div class="flex space-x-2">
          <select v-model="filterCategory" class="input-field">
            <option value="All">All Categories</option>
            <option value="Incident Response">Incident Response</option>
            <option value="Enrichment">Enrichment</option>
            <option value="Email Security">Email Security</option>
            <option value="Vulnerability Management">Vulnerability Management</option>
            <option value="Cloud Security">Cloud Security</option>
            <option value="Identity">Identity</option>
            <option value="Threat Intelligence">Threat Intelligence</option>
          </select>
          <select v-model="filterStatus" class="input-field">
            <option value="All">All Status</option>
            <option value="Active">Active</option>
            <option value="Testing">Testing</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="playbook in filteredPlaybooks"
          :key="playbook.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          @click="$router.push(`/playbooks/${playbook.id}`)"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ playbook.name }}</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ playbook.category }}</p>
            </div>
            <span :class="[
              'badge',
              playbook.status === 'Active' ? 'badge-success' : playbook.status === 'Testing' ? 'badge-warning' : 'badge-danger'
            ]">
              {{ playbook.status }}
            </span>
          </div>

          <p class="text-sm text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">{{ playbook.description }}</p>

          <div class="space-y-2 mb-4">
            <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Avg: {{ playbook.avgExecutionTime }}
            </div>
            <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Success: {{ playbook.successRate }}%
            </div>
          </div>

          <div class="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
            <span class="text-xs text-gray-500 dark:text-gray-400">v{{ playbook.version }}</span>
            <button
              @click.stop="executePlaybook(playbook.id)"
              class="text-xs btn-primary py-1 px-3"
              :disabled="executing === playbook.id"
            >
              {{ executing === playbook.id ? 'Running...' : 'Execute' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="filteredPlaybooks.length === 0" class="text-center py-12">
        <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-gray-500 dark:text-gray-400">No playbooks found</p>
      </div>
    </div>

    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Create New Playbook</h3>
            <button @click="showCreateModal = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="createPlaybook" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Name</label>
              <input v-model="newPlaybook.name" type="text" required class="input-field" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
              <textarea v-model="newPlaybook.description" rows="3" required class="input-field"></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category</label>
              <select v-model="newPlaybook.category" required class="input-field">
                <option value="Incident Response">Incident Response</option>
                <option value="Enrichment">Enrichment</option>
                <option value="Email Security">Email Security</option>
                <option value="Vulnerability Management">Vulnerability Management</option>
                <option value="Cloud Security">Cloud Security</option>
                <option value="Identity">Identity</option>
                <option value="Threat Intelligence">Threat Intelligence</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Language</label>
              <select v-model="newPlaybook.language" required class="input-field">
                <option value="Python">Python</option>
                <option value="PowerShell">PowerShell</option>
                <option value="Bash">Bash</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Owner</label>
              <input v-model="newPlaybook.owner" type="text" required class="input-field" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Triggers (comma-separated)</label>
              <input v-model="triggersInput" type="text" placeholder="e.g., Alert Created, Manual Trigger" class="input-field" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Steps (comma-separated)</label>
              <input v-model="stepsInput" type="text" placeholder="e.g., Parse data, Enrich, Execute action" class="input-field" />
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button type="button" @click="showCreateModal = false" class="btn-secondary">Cancel</button>
              <button type="submit" class="btn-primary">Create Playbook</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { usePlaybooksStore } from '@/stores/playbooks'
import { useToast } from 'vue-toastification'

const playbooksStore = usePlaybooksStore()
const toast = useToast()

const searchQuery = ref('')
const filterCategory = ref('All')
const filterStatus = ref('All')
const executing = ref(null)
const showCreateModal = ref(false)

const newPlaybook = ref({
  name: '',
  description: '',
  category: 'Incident Response',
  language: 'Python',
  owner: ''
})

const triggersInput = ref('')
const stepsInput = ref('')

const filteredPlaybooks = computed(() => {
  let filtered = playbooksStore.playbooks

  if (searchQuery.value) {
    filtered = filtered.filter(p =>
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      p.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (filterCategory.value !== 'All') {
    filtered = filtered.filter(p => p.category === filterCategory.value)
  }

  if (filterStatus.value !== 'All') {
    filtered = filtered.filter(p => p.status === filterStatus.value)
  }

  return filtered
})

async function executePlaybook(id) {
  executing.value = id
  try {
    const result = await playbooksStore.executePlaybook(id)
    if (result.status === 'Success') {
      toast.success('Playbook executed successfully')
    } else {
      toast.error('Playbook execution failed')
    }
  } catch (error) {
    toast.error('Failed to execute playbook')
  } finally {
    executing.value = null
  }
}

function createPlaybook() {
  const playbookData = {
    ...newPlaybook.value,
    triggers: triggersInput.value.split(',').map(t => t.trim()).filter(t => t),
    steps: stepsInput.value.split(',').map(s => s.trim()).filter(s => s)
  }

  playbooksStore.createPlaybook(playbookData)
  toast.success('Playbook created successfully')
  
  showCreateModal.value = false
  newPlaybook.value = {
    name: '',
    description: '',
    category: 'Incident Response',
    language: 'Python',
    owner: ''
  }
  triggersInput.value = ''
  stepsInput.value = ''
}
</script>
