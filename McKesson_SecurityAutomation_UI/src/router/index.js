import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Playbooks from '@/views/Playbooks.vue'
import PlaybookDetail from '@/views/PlaybookDetail.vue'
import SelfService from '@/views/SelfService.vue'
import Integrations from '@/views/Integrations.vue'
import CICD from '@/views/CICD.vue'
import Observability from '@/views/Observability.vue'
import Collaboration from '@/views/Collaboration.vue'
import Settings from '@/views/Settings.vue'
import KubernetesMonitor from '@/views/KubernetesMonitor.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard' }
  },
  {
    path: '/playbooks',
    name: 'Playbooks',
    component: Playbooks,
    meta: { title: 'Playbooks & Scripts' }
  },
  {
    path: '/playbooks/:id',
    name: 'PlaybookDetail',
    component: PlaybookDetail,
    meta: { title: 'Playbook Details' }
  },
  {
    path: '/self-service',
    name: 'SelfService',
    component: SelfService,
    meta: { title: 'Self-Service Portal' }
  },
  {
    path: '/integrations',
    name: 'Integrations',
    component: Integrations,
    meta: { title: 'API Integrations' }
  },
  {
    path: '/cicd',
    name: 'CICD',
    component: CICD,
    meta: { title: 'CI/CD Workflows' }
  },
  {
    path: '/observability',
    name: 'Observability',
    component: Observability,
    meta: { title: 'Observability & Monitoring' }
  },
  {
    path: '/kubernetes',
    name: 'KubernetesMonitor',
    component: KubernetesMonitor,
    meta: { title: 'Kubernetes Monitor' }
  },
  {
    path: '/collaboration',
    name: 'Collaboration',
    component: Collaboration,
    meta: { title: 'Collaboration Hub' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { title: 'Settings' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - Cyber Automation Platform` || 'Cyber Automation Platform'
  next()
})

export default router
