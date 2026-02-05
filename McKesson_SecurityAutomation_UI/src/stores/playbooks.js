import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePlaybooksStore = defineStore('playbooks', () => {
  const playbooks = ref([
    {
      id: 1,
      name: 'Endpoint Remediation',
      description: 'Automated endpoint isolation and remediation for malware detection',
      language: 'Python',
      triggers: ['Malware Alert', 'EDR High Severity'],
      steps: ['Enrich endpoint data', 'Analyze threat severity', 'Isolate endpoint', 'Remediate threat', 'Collect evidence'],
      status: 'Active',
      lastRun: '2026-02-04T10:30:00',
      successRate: 94,
      avgExecutionTime: '2.5 min',
      category: 'Incident Response',
      owner: 'IR Team',
      version: '2.3.1'
    },
    {
      id: 2,
      name: 'SIEM Alert Enrichment',
      description: 'Enriches SIEM alerts with threat intelligence and context',
      language: 'Python',
      triggers: ['SIEM Alert Created'],
      steps: ['Parse alert data', 'Query threat intel feeds', 'Enrich with CMDB data', 'Calculate risk score', 'Update alert'],
      status: 'Active',
      lastRun: '2026-02-04T14:15:00',
      successRate: 98,
      avgExecutionTime: '45 sec',
      category: 'Enrichment',
      owner: 'Security Team',
      version: '3.1.0'
    },
    {
      id: 3,
      name: 'Phishing Email Response',
      description: 'Automated response to phishing email reports',
      language: 'Python',
      triggers: ['Phishing Report', 'Email Security Alert'],
      steps: ['Extract email headers', 'Analyze URLs and attachments', 'Block sender', 'Remove from mailboxes', 'Notify users'],
      status: 'Active',
      lastRun: '2026-02-04T13:45:00',
      successRate: 91,
      avgExecutionTime: '3.2 min',
      category: 'Email Security',
      owner: 'Security Team',
      version: '1.8.2'
    },
    {
      id: 4,
      name: 'Vulnerability Scan Orchestration',
      description: 'Orchestrates vulnerability scans across infrastructure',
      language: 'Python',
      triggers: ['Scheduled', 'New Asset Detected'],
      steps: ['Identify scan targets', 'Execute vulnerability scan', 'Parse results', 'Create tickets', 'Notify owners'],
      status: 'Active',
      lastRun: '2026-02-03T22:00:00',
      successRate: 96,
      avgExecutionTime: '15 min',
      category: 'Vulnerability Management',
      owner: 'Platform Team',
      version: '2.0.5'
    },
    {
      id: 5,
      name: 'Cloud Security Compliance Check',
      description: 'Validates cloud resources against security policies',
      language: 'Python',
      triggers: ['Scheduled', 'Resource Created'],
      steps: ['Scan cloud resources', 'Check compliance rules', 'Generate findings', 'Auto-remediate', 'Create audit log'],
      status: 'Active',
      lastRun: '2026-02-04T12:00:00',
      successRate: 89,
      avgExecutionTime: '8 min',
      category: 'Cloud Security',
      owner: 'Cloud Team',
      version: '1.5.3'
    },
    {
      id: 6,
      name: 'Identity Access Review',
      description: 'Automated periodic access review and certification',
      language: 'Python',
      triggers: ['Scheduled Monthly'],
      steps: ['Collect access data', 'Identify anomalies', 'Generate review reports', 'Send to managers', 'Track responses'],
      status: 'Testing',
      lastRun: '2026-02-01T08:00:00',
      successRate: 85,
      avgExecutionTime: '20 min',
      category: 'Identity',
      owner: 'IAM Team',
      version: '0.9.1'
    },
    {
      id: 7,
      name: 'Threat Intelligence Ingestion',
      description: 'Ingests and normalizes threat intelligence from multiple feeds',
      language: 'Python',
      triggers: ['Scheduled Hourly'],
      steps: ['Fetch threat feeds', 'Normalize indicators', 'Deduplicate', 'Enrich with context', 'Update SIEM'],
      status: 'Active',
      lastRun: '2026-02-04T15:00:00',
      successRate: 99,
      avgExecutionTime: '5 min',
      category: 'Threat Intelligence',
      owner: 'Threat Intel',
      version: '4.2.0'
    },
    {
      id: 8,
      name: 'Incident Response Orchestration',
      description: 'Orchestrates full incident response lifecycle',
      language: 'Python',
      triggers: ['Critical Alert', 'Manual Trigger'],
      steps: ['Create incident', 'Assemble team', 'Execute containment', 'Collect evidence', 'Eradicate threat', 'Document'],
      status: 'Active',
      lastRun: '2026-02-04T09:20:00',
      successRate: 92,
      avgExecutionTime: '25 min',
      category: 'Incident Response',
      owner: 'IR Team',
      version: '3.0.2'
    },
    {
      id: 9,
      name: 'Compliance Evidence Collection',
      description: 'Automated collection of compliance evidence',
      language: 'Python',
      triggers: ['Scheduled Weekly'],
      steps: ['Identify requirements', 'Collect evidence', 'Validate completeness', 'Generate reports', 'Archive securely'],
      status: 'Testing',
      lastRun: '2026-02-02T06:00:00',
      successRate: 87,
      avgExecutionTime: '30 min',
      category: 'Compliance',
      owner: 'Compliance',
      version: '1.2.0'
    },
    {
      id: 10,
      name: 'Network Anomaly Detection',
      description: 'Detects and responds to network anomalies',
      language: 'Python',
      triggers: ['Network Alert', 'Scheduled'],
      steps: ['Analyze traffic patterns', 'Detect anomalies', 'Correlate with threats', 'Alert SOC', 'Auto-block if critical'],
      status: 'Active',
      lastRun: '2026-02-04T14:30:00',
      successRate: 90,
      avgExecutionTime: '4 min',
      category: 'Network Security',
      owner: 'Network Ops',
      version: '2.1.4'
    },
    {
      id: 11,
      name: 'User Behavior Analytics',
      description: 'Analyzes user behavior for insider threats',
      language: 'Python',
      triggers: ['Scheduled Daily'],
      steps: ['Collect user activity', 'Build baseline', 'Detect deviations', 'Risk scoring', 'Alert on high risk'],
      status: 'Active',
      lastRun: '2026-02-04T07:00:00',
      successRate: 88,
      avgExecutionTime: '12 min',
      category: 'Insider Threat',
      owner: 'Security Team',
      version: '1.7.0'
    },
    {
      id: 12,
      name: 'Data Loss Prevention Response',
      description: 'Automated response to DLP policy violations',
      language: 'Python',
      triggers: ['DLP Alert'],
      steps: ['Parse DLP event', 'Classify data', 'Block transfer', 'Notify user', 'Create incident'],
      status: 'Active',
      lastRun: '2026-02-04T11:20:00',
      successRate: 93,
      avgExecutionTime: '1.5 min',
      category: 'Data Security',
      owner: 'Security Team',
      version: '2.4.1'
    }
  ])

  const executions = ref([
    { id: 1, playbookId: 1, status: 'Success', startTime: '2026-02-04T10:30:00', duration: '2m 25s', triggeredBy: 'EDR Alert #4521' },
    { id: 2, playbookId: 2, status: 'Success', startTime: '2026-02-04T14:15:00', duration: '42s', triggeredBy: 'SIEM Alert #8932' },
    { id: 3, playbookId: 3, status: 'Success', startTime: '2026-02-04T13:45:00', duration: '3m 10s', triggeredBy: 'Phishing Report #1234' },
    { id: 4, playbookId: 1, status: 'Failed', startTime: '2026-02-04T09:15:00', duration: '1m 5s', triggeredBy: 'EDR Alert #4518', error: 'Endpoint unreachable' },
    { id: 5, playbookId: 7, status: 'Success', startTime: '2026-02-04T15:00:00', duration: '4m 55s', triggeredBy: 'Scheduled' }
  ])

  function getPlaybookById(id) {
    return playbooks.value.find(p => p.id === parseInt(id))
  }

  function executePlaybook(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const execution = {
          id: executions.value.length + 1,
          playbookId: id,
          status: Math.random() > 0.1 ? 'Success' : 'Failed',
          startTime: new Date().toISOString(),
          duration: `${Math.floor(Math.random() * 5) + 1}m ${Math.floor(Math.random() * 60)}s`,
          triggeredBy: 'Manual Execution'
        }
        if (execution.status === 'Failed') {
          execution.error = 'Simulated failure for testing'
        }
        executions.value.unshift(execution)
        resolve(execution)
      }, 2000)
    })
  }

  function createPlaybook(playbook) {
    const newPlaybook = {
      ...playbook,
      id: Math.max(...playbooks.value.map(p => p.id)) + 1,
      status: 'Testing',
      lastRun: null,
      successRate: 0,
      avgExecutionTime: 'N/A',
      version: '1.0.0'
    }
    playbooks.value.unshift(newPlaybook)
    return newPlaybook
  }

  function updatePlaybook(id, updates) {
    const index = playbooks.value.findIndex(p => p.id === id)
    if (index !== -1) {
      playbooks.value[index] = { ...playbooks.value[index], ...updates }
      return playbooks.value[index]
    }
    return null
  }

  return {
    playbooks,
    executions,
    getPlaybookById,
    executePlaybook,
    createPlaybook,
    updatePlaybook
  }
})
