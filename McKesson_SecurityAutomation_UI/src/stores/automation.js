import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAutomationStore = defineStore('automation', () => {
  const roadmaps = ref([
    { id: 1, useCase: 'Automate SIEM Alert Triage', priority: 'High', status: 'In Progress', impact: '20% toil reduction', quarter: 'Q1 2026', owner: 'Security Team' },
    { id: 2, useCase: 'Endpoint Remediation Automation', priority: 'High', status: 'Completed', impact: '35% toil reduction', quarter: 'Q4 2025', owner: 'IR Team' },
    { id: 3, useCase: 'Vulnerability Scan Orchestration', priority: 'Medium', status: 'In Progress', impact: '15% toil reduction', quarter: 'Q1 2026', owner: 'Platform Team' },
    { id: 4, useCase: 'Email Security Auto-Response', priority: 'High', status: 'Planning', impact: '25% toil reduction', quarter: 'Q2 2026', owner: 'Security Team' },
    { id: 5, useCase: 'Cloud Security Posture Management', priority: 'Medium', status: 'In Progress', impact: '18% toil reduction', quarter: 'Q1 2026', owner: 'Cloud Team' },
    { id: 6, useCase: 'Identity Access Review Automation', priority: 'Low', status: 'Planning', impact: '10% toil reduction', quarter: 'Q2 2026', owner: 'IAM Team' },
    { id: 7, useCase: 'Threat Intelligence Enrichment', priority: 'High', status: 'Completed', impact: '30% toil reduction', quarter: 'Q4 2025', owner: 'Threat Intel' },
    { id: 8, useCase: 'Incident Response Playbook Execution', priority: 'High', status: 'In Progress', impact: '40% toil reduction', quarter: 'Q1 2026', owner: 'IR Team' },
    { id: 9, useCase: 'Compliance Evidence Collection', priority: 'Medium', status: 'Planning', impact: '22% toil reduction', quarter: 'Q2 2026', owner: 'Compliance' },
    { id: 10, useCase: 'Network Anomaly Detection', priority: 'Medium', status: 'In Progress', impact: '12% toil reduction', quarter: 'Q1 2026', owner: 'Network Ops' }
  ])

  const metrics = ref({
    toilReduction: [
      { month: 'Aug', value: 12 },
      { month: 'Sep', value: 18 },
      { month: 'Oct', value: 25 },
      { month: 'Nov', value: 32 },
      { month: 'Dec', value: 38 },
      { month: 'Jan', value: 45 }
    ],
    playbookSuccess: [
      { month: 'Aug', value: 78 },
      { month: 'Sep', value: 82 },
      { month: 'Oct', value: 85 },
      { month: 'Nov', value: 88 },
      { month: 'Dec', value: 91 },
      { month: 'Jan', value: 94 }
    ],
    latency: [
      { month: 'Aug', value: 450 },
      { month: 'Sep', value: 420 },
      { month: 'Oct', value: 380 },
      { month: 'Nov', value: 350 },
      { month: 'Dec', value: 320 },
      { month: 'Jan', value: 280 }
    ],
    coverage: {
      'SIEM/SOAR': 92,
      'Endpoint/EDR': 88,
      'Vulnerability Mgmt': 75,
      'Email/Data Security': 82,
      'Cloud Security': 78,
      'Identity': 70
    }
  })

  const objectives = ref([
    { id: 1, quarter: 'Q1 2026', title: 'Reduce manual SIEM triage by 50%', progress: 65, status: 'On Track' },
    { id: 2, quarter: 'Q1 2026', title: 'Achieve 95% playbook success rate', progress: 85, status: 'On Track' },
    { id: 3, quarter: 'Q1 2026', title: 'Deploy 15 new automation workflows', progress: 40, status: 'At Risk' },
    { id: 4, quarter: 'Q2 2026', title: 'Integrate 10 new security tools', progress: 20, status: 'Planning' }
  ])

  const totalToilReduction = computed(() => {
    return roadmaps.value
      .filter(r => r.status === 'Completed')
      .reduce((sum, r) => sum + parseInt(r.impact), 0)
  })

  const activeAutomations = computed(() => {
    return roadmaps.value.filter(r => r.status === 'In Progress').length
  })

  const completedAutomations = computed(() => {
    return roadmaps.value.filter(r => r.status === 'Completed').length
  })

  return {
    roadmaps,
    metrics,
    objectives,
    totalToilReduction,
    activeAutomations,
    completedAutomations
  }
})
