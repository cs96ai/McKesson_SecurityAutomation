<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Self-Service Portal</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Execute standardized security actions safely</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">CLI Simulator</h3>
          <div class="bg-gray-900 rounded-lg p-4 font-mono text-sm">
            <div class="space-y-1 mb-4 max-h-96 overflow-y-auto">
              <div v-for="(line, index) in terminalOutput" :key="index" :class="line.type === 'error' ? 'text-red-400' : line.type === 'success' ? 'text-green-400' : 'text-gray-300'">
                {{ line.text }}
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-green-400">$</span>
              <input
                v-model="cliCommand"
                @keyup.enter="executeCommand"
                type="text"
                class="flex-1 bg-transparent border-none outline-none text-gray-100"
                placeholder="Type a command (try: help, list-alerts, isolate-endpoint, scan-vulnerability)"
                :disabled="executing"
              />
            </div>
          </div>
          <div class="mt-4 flex flex-wrap gap-2">
            <button @click="cliCommand = 'help'; executeCommand()" class="btn-secondary text-xs py-1 px-3">help</button>
            <button @click="cliCommand = 'list-alerts'; executeCommand()" class="btn-secondary text-xs py-1 px-3">list-alerts</button>
            <button @click="cliCommand = 'isolate-endpoint 192.168.1.100'; executeCommand()" class="btn-secondary text-xs py-1 px-3">isolate-endpoint</button>
            <button @click="cliCommand = 'scan-vulnerability'; executeCommand()" class="btn-secondary text-xs py-1 px-3">scan-vulnerability</button>
            <button @click="terminalOutput = [{ text: 'Terminal cleared', type: 'info' }]" class="btn-secondary text-xs py-1 px-3">clear</button>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">ChatOps Interface</h3>
          <div class="border border-gray-200 dark:border-gray-700 rounded-lg">
            <div class="bg-gray-50 dark:bg-gray-700 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center space-x-2">
                <div class="w-8 h-8 bg-primary-600 rounded flex items-center justify-center text-white text-sm font-medium">
                  CA
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">CyberAuto Bot</p>
                  <p class="text-xs text-green-600 dark:text-green-400">● Online</p>
                </div>
              </div>
            </div>
            
            <div class="p-4 space-y-4 max-h-96 overflow-y-auto">
              <div v-for="(message, index) in chatMessages" :key="index" :class="message.sender === 'user' ? 'flex justify-end' : 'flex justify-start'">
                <div :class="message.sender === 'user' ? 'bg-primary-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white'" class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
                  <p class="text-sm">{{ message.text }}</p>
                  <p class="text-xs mt-1 opacity-70">{{ message.time }}</p>
                </div>
              </div>
            </div>

            <div class="p-4 border-t border-gray-200 dark:border-gray-700">
              <div class="flex space-x-2">
                <input
                  v-model="chatMessage"
                  @keyup.enter="sendChatMessage"
                  type="text"
                  placeholder="Type a message... (e.g., 'triage alert #8932', 'block IP 10.0.0.5')"
                  class="input-field flex-1"
                  :disabled="executing"
                />
                <button @click="sendChatMessage" :disabled="executing" class="btn-primary">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
          <div class="space-y-2">
            <button @click="executeQuickAction('Triage Alert')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Triage Alert</span>
              </div>
            </button>

            <button @click="executeQuickAction('Isolate Endpoint')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Isolate Endpoint</span>
              </div>
            </button>

            <button @click="executeQuickAction('Block IP')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m-4.243 2.829a4.978 4.978 0 01-1.414-2.83m-1.414 5.658a9 9 0 01-2.167-9.238m7.824 2.167a1 1 0 111.414 1.414m-1.414-1.414L3 3" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Block IP</span>
              </div>
            </button>

            <button @click="executeQuickAction('Reset Password')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Reset Password</span>
              </div>
            </button>

            <button @click="executeQuickAction('Collect Evidence')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Collect Evidence</span>
              </div>
            </button>

            <button @click="executeQuickAction('Run Vulnerability Scan')" class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <div class="flex items-center space-x-3">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                <span class="text-sm font-medium text-gray-900 dark:text-white">Run Vulnerability Scan</span>
              </div>
            </button>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Actions</h3>
          <div class="space-y-3">
            <div v-for="action in recentActions" :key="action.id" class="text-sm">
              <div class="flex items-center justify-between">
                <span class="font-medium text-gray-900 dark:text-white">{{ action.action }}</span>
                <span :class="[
                  'badge',
                  action.status === 'Success' ? 'badge-success' : 'badge-danger'
                ]">
                  {{ action.status }}
                </span>
              </div>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ action.timestamp }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()

const cliCommand = ref('')
const executing = ref(false)
const terminalOutput = ref([
  { text: 'CyberAuto Self-Service CLI v2.3.1', type: 'info' },
  { text: 'Type "help" for available commands', type: 'info' }
])

const chatMessage = ref('')
const chatMessages = ref([
  { sender: 'bot', text: 'Hello! I\'m CyberAuto Bot. How can I help you today?', time: '10:00 AM' }
])

const recentActions = ref([
  { id: 1, action: 'Triage Alert #8932', status: 'Success', timestamp: '2 minutes ago' },
  { id: 2, action: 'Isolate Endpoint 192.168.1.100', status: 'Success', timestamp: '15 minutes ago' },
  { id: 3, action: 'Block IP 10.0.0.5', status: 'Success', timestamp: '1 hour ago' },
  { id: 4, action: 'Reset Password user@company.com', status: 'Success', timestamp: '2 hours ago' }
])

const commands = {
  help: () => [
    { text: 'Available commands:', type: 'info' },
    { text: '  help - Show this help message', type: 'info' },
    { text: '  list-alerts - List recent security alerts', type: 'info' },
    { text: '  isolate-endpoint <ip> - Isolate an endpoint', type: 'info' },
    { text: '  block-ip <ip> - Block an IP address', type: 'info' },
    { text: '  scan-vulnerability - Run vulnerability scan', type: 'info' },
    { text: '  collect-evidence <incident-id> - Collect incident evidence', type: 'info' }
  ],
  'list-alerts': () => [
    { text: 'Recent Security Alerts:', type: 'info' },
    { text: '  #8932 - High - Malware detected on endpoint', type: 'info' },
    { text: '  #8931 - Medium - Suspicious login attempt', type: 'info' },
    { text: '  #8930 - Low - Failed authentication', type: 'info' }
  ],
  'isolate-endpoint': (args) => {
    const ip = args[0] || '192.168.1.100'
    return [
      { text: `Isolating endpoint ${ip}...`, type: 'info' },
      { text: 'Endpoint isolated successfully', type: 'success' },
      { text: 'Evidence collected and stored', type: 'success' }
    ]
  },
  'block-ip': (args) => {
    const ip = args[0] || '10.0.0.5'
    return [
      { text: `Blocking IP ${ip}...`, type: 'info' },
      { text: 'IP blocked on firewall', type: 'success' },
      { text: 'Alert created for monitoring', type: 'success' }
    ]
  },
  'scan-vulnerability': () => [
    { text: 'Starting vulnerability scan...', type: 'info' },
    { text: 'Scanning 342 assets...', type: 'info' },
    { text: 'Scan completed: 87 vulnerabilities found', type: 'success' },
    { text: 'Report generated: /reports/vuln-scan-2026-02-04.pdf', type: 'success' }
  ],
  'collect-evidence': (args) => {
    const incidentId = args[0] || 'IR-2026-045'
    return [
      { text: `Collecting evidence for incident ${incidentId}...`, type: 'info' },
      { text: 'Collecting logs from affected systems...', type: 'info' },
      { text: 'Evidence package created', type: 'success' },
      { text: 'Evidence stored securely', type: 'success' }
    ]
  }
}

function executeCommand() {
  if (!cliCommand.value.trim()) return

  executing.value = true
  terminalOutput.value.push({ text: `$ ${cliCommand.value}`, type: 'command' })

  setTimeout(() => {
    const parts = cliCommand.value.trim().split(' ')
    const cmd = parts[0]
    const args = parts.slice(1)

    if (commands[cmd]) {
      const output = commands[cmd](args)
      terminalOutput.value.push(...output)
    } else {
      terminalOutput.value.push({ text: `Command not found: ${cmd}. Type "help" for available commands.`, type: 'error' })
    }

    cliCommand.value = ''
    executing.value = false
  }, 500)
}

function sendChatMessage() {
  if (!chatMessage.value.trim()) return

  const userMessage = chatMessage.value
  chatMessages.value.push({
    sender: 'user',
    text: userMessage,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  })

  chatMessage.value = ''
  executing.value = true

  setTimeout(() => {
    let response = 'I\'ve processed your request. '
    
    if (userMessage.toLowerCase().includes('triage')) {
      response += 'Alert has been triaged and enriched with threat intelligence. Risk score: High. Recommended action: Isolate endpoint.'
    } else if (userMessage.toLowerCase().includes('block')) {
      response += 'IP address has been blocked on the firewall. Monitoring alert created.'
    } else if (userMessage.toLowerCase().includes('isolate')) {
      response += 'Endpoint has been isolated from the network. Evidence collection initiated.'
    } else {
      response += 'Action completed successfully. Check the audit log for details.'
    }

    chatMessages.value.push({
      sender: 'bot',
      text: response,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    })

    executing.value = false
  }, 1000)
}

function executeQuickAction(action) {
  toast.info(`Executing: ${action}`)
  
  setTimeout(() => {
    recentActions.value.unshift({
      id: Date.now(),
      action: action,
      status: Math.random() > 0.1 ? 'Success' : 'Failed',
      timestamp: 'Just now'
    })
    
    if (recentActions.value.length > 10) {
      recentActions.value.pop()
    }
    
    toast.success(`${action} completed successfully`)
  }, 1500)
}
</script>
