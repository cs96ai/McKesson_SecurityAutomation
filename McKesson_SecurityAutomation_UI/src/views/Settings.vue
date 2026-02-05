<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Settings</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage your profile and preferences</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Profile Information</h3>
          <form @submit.prevent="saveProfile" class="space-y-4">
            <div class="flex items-center space-x-4 mb-6">
              <img :src="userStore.currentUser.avatar" alt="Avatar" class="w-20 h-20 rounded-full" />
              <div>
                <button type="button" class="btn-secondary text-sm">Change Avatar</button>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">JPG, PNG or GIF. Max 2MB.</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
                <input v-model="profile.name" type="text" required class="input-field" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                <input v-model="profile.email" type="email" required class="input-field" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <select v-model="profile.role" class="input-field">
                  <option value="Admin">Admin</option>
                  <option value="User">User</option>
                  <option value="Viewer">Viewer</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Team</label>
                <input v-model="profile.team" type="text" class="input-field" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Timezone</label>
                <select v-model="profile.timezone" class="input-field">
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                  <option value="UTC">UTC</option>
                </select>
              </div>
            </div>

            <div class="flex justify-end pt-4">
              <button type="submit" class="btn-primary">Save Changes</button>
            </div>
          </form>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Skills & Expertise</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Technical Skills</label>
              <div class="flex flex-wrap gap-2 mb-3">
                <span
                  v-for="(skill, index) in profile.skills"
                  :key="index"
                  class="badge badge-info flex items-center space-x-1"
                >
                  <span>{{ skill }}</span>
                  <button @click="removeSkill(index)" class="ml-1 hover:text-red-600">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
              </div>
              <div class="flex space-x-2">
                <input
                  v-model="newSkill"
                  @keyup.enter="addSkill"
                  type="text"
                  placeholder="Add a skill (e.g., Python, Terraform)"
                  class="input-field flex-1"
                />
                <button @click="addSkill" type="button" class="btn-primary">Add</button>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Preferences</h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Dark Mode</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Use dark theme across the application</p>
              </div>
              <button
                @click="userStore.toggleDarkMode()"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  userStore.darkMode ? 'bg-primary-600' : 'bg-gray-300'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    userStore.darkMode ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Notifications</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Receive in-app notifications</p>
              </div>
              <button
                @click="togglePreference('notifications')"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  preferences.notifications ? 'bg-primary-600' : 'bg-gray-300'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    preferences.notifications ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>

            <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Email Alerts</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Receive email notifications for critical alerts</p>
              </div>
              <button
                @click="togglePreference('emailAlerts')"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  preferences.emailAlerts ? 'bg-primary-600' : 'bg-gray-300'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    preferences.emailAlerts ? 'translate-x-6' : 'translate-x-1'
                  ]"
                ></span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="space-y-6">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Account</h3>
          <div class="space-y-3">
            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Account Type</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ userStore.currentUser.role }}</p>
            </div>
            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Member Since</p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">January 2024</p>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Security</h3>
          <div class="space-y-2">
            <button class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Change Password</p>
            </button>
            <button class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Two-Factor Authentication</p>
            </button>
            <button class="w-full text-left px-4 py-3 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 rounded-lg transition-colors">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Active Sessions</p>
            </button>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Danger Zone</h3>
          <button class="w-full btn-danger text-sm">
            Delete Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useToast } from 'vue-toastification'

const userStore = useUserStore()
const toast = useToast()

const profile = reactive({
  name: userStore.currentUser.name,
  email: userStore.currentUser.email,
  role: userStore.currentUser.role,
  team: userStore.currentUser.team,
  timezone: userStore.currentUser.timezone,
  skills: [...userStore.currentUser.skills]
})

const preferences = reactive({
  notifications: userStore.currentUser.preferences.notifications,
  emailAlerts: userStore.currentUser.preferences.emailAlerts
})

const newSkill = ref('')

function saveProfile() {
  userStore.updateProfile(profile)
  toast.success('Profile updated successfully')
}

function addSkill() {
  if (newSkill.value.trim() && !profile.skills.includes(newSkill.value.trim())) {
    profile.skills.push(newSkill.value.trim())
    newSkill.value = ''
  }
}

function removeSkill(index) {
  profile.skills.splice(index, 1)
}

function togglePreference(key) {
  preferences[key] = !preferences[key]
  userStore.updatePreferences(preferences)
  toast.success('Preferences updated')
}
</script>
