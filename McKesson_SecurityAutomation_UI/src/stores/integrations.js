import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useIntegrationsStore = defineStore('integrations', () => {
  const integrations = ref([
    {
      id: 1,
      tool: 'Splunk',
      category: 'SIEM/SOAR',
      integratedWith: ['ServiceNow', 'Cortex XSOAR', 'Slack'],
      status: 'Active',
      lastSync: '2026-02-04T15:30:00',
      authType: 'OAuth2',
      endpoint: 'https://splunk.company.com/api/v1',
      requestsPerDay: 15420,
      errorRate: 0.2
    },
    {
      id: 2,
      tool: 'Cortex XSOAR',
      category: 'SIEM/SOAR',
      integratedWith: ['Splunk', 'SentinelOne', 'Rapid7', 'Microsoft Defender'],
      status: 'Active',
      lastSync: '2026-02-04T15:28:00',
      authType: 'API Key',
      endpoint: 'https://xsoar.company.com/api',
      requestsPerDay: 8930,
      errorRate: 0.5
    },
    {
      id: 3,
      tool: 'SentinelOne',
      category: 'Endpoint/EDR',
      integratedWith: ['Cortex XSOAR', 'ServiceNow', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:25:00',
      authType: 'Bearer Token',
      endpoint: 'https://api.sentinelone.net/web/api/v2.1',
      requestsPerDay: 12340,
      errorRate: 0.3
    },
    {
      id: 4,
      tool: 'ServiceNow',
      category: 'ITSM',
      integratedWith: ['Splunk', 'Cortex XSOAR', 'Rapid7', 'Azure AD'],
      status: 'Active',
      lastSync: '2026-02-04T15:29:00',
      authType: 'OAuth2',
      endpoint: 'https://company.service-now.com/api',
      requestsPerDay: 23450,
      errorRate: 0.1
    },
    {
      id: 5,
      tool: 'Rapid7 InsightVM',
      category: 'Vulnerability Management',
      integratedWith: ['ServiceNow', 'Cortex XSOAR', 'Jira'],
      status: 'Active',
      lastSync: '2026-02-04T15:20:00',
      authType: 'API Key',
      endpoint: 'https://us.api.insight.rapid7.com',
      requestsPerDay: 5670,
      errorRate: 0.4
    },
    {
      id: 6,
      tool: 'Microsoft Defender',
      category: 'Endpoint/EDR',
      integratedWith: ['Cortex XSOAR', 'Azure Sentinel', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:27:00',
      authType: 'OAuth2',
      endpoint: 'https://api.securitycenter.microsoft.com/api',
      requestsPerDay: 18920,
      errorRate: 0.2
    },
    {
      id: 7,
      tool: 'Proofpoint',
      category: 'Email Security',
      integratedWith: ['Cortex XSOAR', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:22:00',
      authType: 'Basic Auth',
      endpoint: 'https://tap-api-v2.proofpoint.com/v2',
      requestsPerDay: 7890,
      errorRate: 0.3
    },
    {
      id: 8,
      tool: 'Azure AD',
      category: 'Identity',
      integratedWith: ['ServiceNow', 'Splunk', 'Okta'],
      status: 'Active',
      lastSync: '2026-02-04T15:31:00',
      authType: 'OAuth2',
      endpoint: 'https://graph.microsoft.com/v1.0',
      requestsPerDay: 34560,
      errorRate: 0.1
    },
    {
      id: 9,
      tool: 'AWS Security Hub',
      category: 'Cloud Security',
      integratedWith: ['Splunk', 'ServiceNow', 'Cortex XSOAR'],
      status: 'Active',
      lastSync: '2026-02-04T15:26:00',
      authType: 'AWS IAM',
      endpoint: 'https://securityhub.us-east-1.amazonaws.com',
      requestsPerDay: 11230,
      errorRate: 0.2
    },
    {
      id: 10,
      tool: 'CrowdStrike',
      category: 'Endpoint/EDR',
      integratedWith: ['Cortex XSOAR', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:24:00',
      authType: 'OAuth2',
      endpoint: 'https://api.crowdstrike.com',
      requestsPerDay: 9870,
      errorRate: 0.3
    },
    {
      id: 11,
      tool: 'Okta',
      category: 'Identity',
      integratedWith: ['Azure AD', 'ServiceNow', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:23:00',
      authType: 'OAuth2',
      endpoint: 'https://company.okta.com/api/v1',
      requestsPerDay: 21340,
      errorRate: 0.2
    },
    {
      id: 12,
      tool: 'Jira',
      category: 'Project Management',
      integratedWith: ['ServiceNow', 'Rapid7', 'GitHub'],
      status: 'Active',
      lastSync: '2026-02-04T15:21:00',
      authType: 'API Token',
      endpoint: 'https://company.atlassian.net/rest/api/3',
      requestsPerDay: 14560,
      errorRate: 0.1
    },
    {
      id: 13,
      tool: 'Palo Alto Prisma Cloud',
      category: 'Cloud Security',
      integratedWith: ['Splunk', 'ServiceNow'],
      status: 'Maintenance',
      lastSync: '2026-02-04T10:00:00',
      authType: 'JWT',
      endpoint: 'https://api.prismacloud.io',
      requestsPerDay: 6780,
      errorRate: 1.2
    },
    {
      id: 14,
      tool: 'Tenable.io',
      category: 'Vulnerability Management',
      integratedWith: ['ServiceNow', 'Splunk'],
      status: 'Active',
      lastSync: '2026-02-04T15:19:00',
      authType: 'API Key',
      endpoint: 'https://cloud.tenable.com/api',
      requestsPerDay: 4320,
      errorRate: 0.4
    },
    {
      id: 15,
      tool: 'Slack',
      category: 'ChatOps',
      integratedWith: ['Splunk', 'Cortex XSOAR', 'PagerDuty'],
      status: 'Active',
      lastSync: '2026-02-04T15:32:00',
      authType: 'OAuth2',
      endpoint: 'https://slack.com/api',
      requestsPerDay: 45670,
      errorRate: 0.1
    }
  ])

  const apiLogs = ref([
    { id: 1, integration: 'Splunk', method: 'POST', endpoint: '/search/jobs', status: 200, duration: '245ms', timestamp: '2026-02-04T15:30:15' },
    { id: 2, integration: 'ServiceNow', method: 'GET', endpoint: '/incident', status: 200, duration: '189ms', timestamp: '2026-02-04T15:29:42' },
    { id: 3, integration: 'SentinelOne', method: 'POST', endpoint: '/threats/mitigate', status: 200, duration: '567ms', timestamp: '2026-02-04T15:25:33' },
    { id: 4, integration: 'Cortex XSOAR', method: 'POST', endpoint: '/incident/create', status: 201, duration: '423ms', timestamp: '2026-02-04T15:28:21' },
    { id: 5, integration: 'Rapid7 InsightVM', method: 'GET', endpoint: '/vulnerabilities', status: 200, duration: '1234ms', timestamp: '2026-02-04T15:20:10' },
    { id: 6, integration: 'Prisma Cloud', method: 'GET', endpoint: '/alerts', status: 500, duration: '5000ms', timestamp: '2026-02-04T10:00:05', error: 'Connection timeout' }
  ])

  function testIntegration(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const integration = integrations.value.find(i => i.id === id)
        const success = Math.random() > 0.1
        const log = {
          id: apiLogs.value.length + 1,
          integration: integration.tool,
          method: 'GET',
          endpoint: '/health',
          status: success ? 200 : 500,
          duration: `${Math.floor(Math.random() * 500) + 100}ms`,
          timestamp: new Date().toISOString(),
          error: success ? null : 'Connection failed'
        }
        apiLogs.value.unshift(log)
        resolve({ success, log })
      }, 1500)
    })
  }

  return {
    integrations,
    apiLogs,
    testIntegration
  }
})
