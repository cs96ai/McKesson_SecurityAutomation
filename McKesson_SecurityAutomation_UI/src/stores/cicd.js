import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCICDStore = defineStore('cicd', () => {
  const pipelines = ref([
    {
      id: 1,
      name: 'Automation Deployment',
      repository: 'security-automation',
      branch: 'main',
      stages: ['Build', 'Test', 'Security Scan', 'Deploy to Dev', 'Deploy to Prod'],
      status: 'Success',
      lastRun: '2026-02-04T14:30:00',
      duration: '8m 45s',
      triggeredBy: 'john.doe@company.com',
      environment: 'Production'
    },
    {
      id: 2,
      name: 'Playbook CI',
      repository: 'security-playbooks',
      branch: 'develop',
      stages: ['Lint', 'Unit Tests', 'Integration Tests', 'Package'],
      status: 'Running',
      lastRun: '2026-02-04T15:20:00',
      duration: '3m 12s',
      triggeredBy: 'jane.smith@company.com',
      environment: 'Development'
    },
    {
      id: 3,
      name: 'Integration Tests',
      repository: 'security-automation',
      branch: 'feature/new-integration',
      stages: ['Build', 'Test', 'Integration Tests'],
      status: 'Failed',
      lastRun: '2026-02-04T13:15:00',
      duration: '5m 23s',
      triggeredBy: 'bob.wilson@company.com',
      environment: 'Development',
      error: 'Integration test failed: API timeout'
    },
    {
      id: 4,
      name: 'Infrastructure as Code',
      repository: 'security-infrastructure',
      branch: 'main',
      stages: ['Validate', 'Plan', 'Apply'],
      status: 'Success',
      lastRun: '2026-02-04T12:00:00',
      duration: '12m 34s',
      triggeredBy: 'alice.brown@company.com',
      environment: 'Production'
    },
    {
      id: 5,
      name: 'SOAR Connector Build',
      repository: 'soar-connectors',
      branch: 'main',
      stages: ['Build', 'Test', 'Package', 'Deploy'],
      status: 'Success',
      lastRun: '2026-02-04T11:30:00',
      duration: '6m 18s',
      triggeredBy: 'charlie.davis@company.com',
      environment: 'Production'
    },
    {
      id: 6,
      name: 'Security Scanning',
      repository: 'security-automation',
      branch: 'main',
      stages: ['SAST', 'DAST', 'Dependency Check', 'Container Scan'],
      status: 'Success',
      lastRun: '2026-02-04T10:00:00',
      duration: '15m 42s',
      triggeredBy: 'Scheduled',
      environment: 'CI'
    }
  ])

  const deployments = ref([
    { id: 1, pipeline: 'Automation Deployment', environment: 'Production', version: 'v2.3.1', status: 'Active', deployedAt: '2026-02-04T14:38:00', deployedBy: 'john.doe@company.com' },
    { id: 2, pipeline: 'Automation Deployment', environment: 'Development', version: 'v2.4.0-beta', status: 'Active', deployedAt: '2026-02-04T15:10:00', deployedBy: 'jane.smith@company.com' },
    { id: 3, pipeline: 'SOAR Connector Build', environment: 'Production', version: 'v1.8.2', status: 'Active', deployedAt: '2026-02-04T11:36:00', deployedBy: 'charlie.davis@company.com' },
    { id: 4, pipeline: 'Infrastructure as Code', environment: 'Production', version: 'v3.1.0', status: 'Active', deployedAt: '2026-02-04T12:12:00', deployedBy: 'alice.brown@company.com' },
    { id: 5, pipeline: 'Automation Deployment', environment: 'Production', version: 'v2.3.0', status: 'Rolled Back', deployedAt: '2026-02-03T16:20:00', deployedBy: 'john.doe@company.com' }
  ])

  const secrets = ref([
    { id: 1, name: 'SPLUNK_API_KEY', scope: 'Production', lastRotated: '2026-01-15', expiresIn: '75 days', status: 'Active' },
    { id: 2, name: 'XSOAR_API_TOKEN', scope: 'Production', lastRotated: '2026-01-20', expiresIn: '80 days', status: 'Active' },
    { id: 3, name: 'SERVICENOW_CLIENT_SECRET', scope: 'Production', lastRotated: '2026-01-10', expiresIn: '70 days', status: 'Active' },
    { id: 4, name: 'AWS_ACCESS_KEY', scope: 'Production', lastRotated: '2025-12-01', expiresIn: '25 days', status: 'Expiring Soon' },
    { id: 5, name: 'AZURE_CLIENT_SECRET', scope: 'Production', lastRotated: '2026-01-25', expiresIn: '85 days', status: 'Active' },
    { id: 6, name: 'GITHUB_TOKEN', scope: 'CI/CD', lastRotated: '2026-02-01', expiresIn: '88 days', status: 'Active' }
  ])

  function runPipeline(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const pipeline = pipelines.value.find(p => p.id === id)
        pipeline.status = 'Running'
        pipeline.lastRun = new Date().toISOString()
        
        setTimeout(() => {
          pipeline.status = Math.random() > 0.2 ? 'Success' : 'Failed'
          pipeline.duration = `${Math.floor(Math.random() * 10) + 3}m ${Math.floor(Math.random() * 60)}s`
          if (pipeline.status === 'Failed') {
            pipeline.error = 'Simulated pipeline failure'
          }
          resolve(pipeline)
        }, 3000)
      }, 500)
    })
  }

  function rollbackDeployment(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const deployment = deployments.value.find(d => d.id === id)
        deployment.status = 'Rolled Back'
        resolve(deployment)
      }, 2000)
    })
  }

  function rotateSecret(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const secret = secrets.value.find(s => s.id === id)
        secret.lastRotated = new Date().toISOString().split('T')[0]
        secret.expiresIn = '90 days'
        secret.status = 'Active'
        resolve(secret)
      }, 1500)
    })
  }

  return {
    pipelines,
    deployments,
    secrets,
    runPipeline,
    rollbackDeployment,
    rotateSecret
  }
})
