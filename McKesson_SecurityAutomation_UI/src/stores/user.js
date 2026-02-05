import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref({
    id: 1,
    name: 'John Doe',
    email: 'john.doe@company.com',
    role: 'Admin',
    avatar: 'https://ui-avatars.com/api/?name=John+Doe&background=3b82f6&color=fff',
    preferences: {
      darkMode: true,
      notifications: true,
      emailAlerts: true
    },
    skills: ['Python', 'Terraform', 'Ansible', 'REST APIs', 'OAuth2', 'Event-Driven Architecture'],
    team: 'Security Automation',
    timezone: 'America/New_York'
  })

  const darkMode = ref(true)
  
  // Initialize dark mode on startup
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  }

  function toggleDarkMode() {
    darkMode.value = !darkMode.value
    currentUser.value.preferences.darkMode = darkMode.value
    
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  function updatePreferences(preferences) {
    currentUser.value.preferences = { ...currentUser.value.preferences, ...preferences }
  }

  function updateProfile(updates) {
    currentUser.value = { ...currentUser.value, ...updates }
  }

  return {
    currentUser,
    darkMode,
    toggleDarkMode,
    updatePreferences,
    updateProfile
  }
})
