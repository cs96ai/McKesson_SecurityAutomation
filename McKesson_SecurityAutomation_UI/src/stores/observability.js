import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useObservabilityStore = defineStore('observability', () => {
  const metrics = ref({
    playbookExecutions: [
      { time: '10:00', success: 45, failed: 2 },
      { time: '11:00', success: 52, failed: 3 },
      { time: '12:00', success: 48, failed: 1 },
      { time: '13:00', success: 61, failed: 4 },
      { time: '14:00', success: 58, failed: 2 },
      { time: '15:00', success: 63, failed: 1 }
    ],
    latency: [
      { time: '10:00', p50: 250, p95: 450, p99: 780 },
      { time: '11:00', p50: 280, p95: 520, p99: 850 },
      { time: '12:00', p50: 240, p95: 480, p99: 720 },
      { time: '13:00', p50: 260, p95: 500, p99: 800 },
      { time: '14:00', p50: 270, p95: 510, p99: 820 },
      { time: '15:00', p50: 255, p95: 490, p99: 760 }
    ],
    errorBudget: {
      current: 99.4,
      target: 99.5,
      remaining: 0.1,
      consumed: 0.5
    }
  })

  const alerts = ref([
    {
      id: 1,
      severity: 'Critical',
      title: 'High Error Rate in Endpoint Remediation',
      description: 'Error rate exceeded 5% threshold',
      timestamp: '2026-02-04T15:25:00',
      status: 'Active',
      affectedService: 'Endpoint Remediation Playbook'
    },
    {
      id: 2,
      severity: 'Warning',
      title: 'Increased Latency in SIEM Integration',
      description: 'P95 latency above 500ms for 10 minutes',
      timestamp: '2026-02-04T14:50:00',
      status: 'Acknowledged',
      affectedService: 'Splunk Integration'
    },
    {
      id: 3,
      severity: 'Info',
      title: 'Scheduled Maintenance Completed',
      description: 'Database maintenance completed successfully',
      timestamp: '2026-02-04T13:00:00',
      status: 'Resolved',
      affectedService: 'Database'
    },
    {
      id: 4,
      severity: 'Warning',
      title: 'API Rate Limit Approaching',
      description: 'ServiceNow API usage at 85% of daily limit',
      timestamp: '2026-02-04T12:30:00',
      status: 'Active',
      affectedService: 'ServiceNow Integration'
    }
  ])

  const logs = ref([
    { id: 1, level: 'INFO', service: 'SIEM Alert Enrichment', message: 'Successfully enriched alert #8932 with threat intel', timestamp: '2026-02-04T15:30:45' },
    { id: 2, level: 'ERROR', service: 'Endpoint Remediation', message: 'Failed to isolate endpoint: Connection timeout', timestamp: '2026-02-04T15:28:12' },
    { id: 3, level: 'INFO', service: 'Phishing Email Response', message: 'Blocked sender and removed 15 emails from mailboxes', timestamp: '2026-02-04T15:25:33' },
    { id: 4, level: 'WARN', service: 'Splunk Integration', message: 'API response time exceeded threshold: 567ms', timestamp: '2026-02-04T15:22:18' },
    { id: 5, level: 'INFO', service: 'Threat Intelligence Ingestion', message: 'Ingested 1,234 new IOCs from 5 feeds', timestamp: '2026-02-04T15:20:00' },
    { id: 6, level: 'ERROR', service: 'Cloud Security Compliance', message: 'Failed to scan AWS account: Invalid credentials', timestamp: '2026-02-04T15:15:42' },
    { id: 7, level: 'INFO', service: 'Vulnerability Scan Orchestration', message: 'Completed scan of 342 assets, found 87 vulnerabilities', timestamp: '2026-02-04T15:10:25' },
    { id: 8, level: 'INFO', service: 'Incident Response Orchestration', message: 'Created incident #IR-2026-045 and assembled response team', timestamp: '2026-02-04T15:05:10' }
  ])

  const traces = ref([
    {
      id: 1,
      traceId: 'trace-abc123',
      service: 'SIEM Alert Enrichment',
      operation: 'enrich_alert',
      duration: '423ms',
      timestamp: '2026-02-04T15:30:45',
      spans: [
        { name: 'parse_alert', duration: '45ms' },
        { name: 'query_threat_intel', duration: '234ms' },
        { name: 'enrich_cmdb', duration: '89ms' },
        { name: 'calculate_risk', duration: '32ms' },
        { name: 'update_alert', duration: '23ms' }
      ]
    },
    {
      id: 2,
      traceId: 'trace-def456',
      service: 'Endpoint Remediation',
      operation: 'remediate_endpoint',
      duration: '2.5s',
      timestamp: '2026-02-04T15:28:12',
      spans: [
        { name: 'enrich_endpoint', duration: '156ms' },
        { name: 'analyze_threat', duration: '234ms' },
        { name: 'isolate_endpoint', duration: '1.8s' },
        { name: 'collect_evidence', duration: '310ms' }
      ]
    }
  ])

  const healthChecks = ref([
    { service: 'Automation Engine', status: 'Healthy', lastCheck: '2026-02-04T15:30:00', uptime: '99.98%' },
    { service: 'Database', status: 'Healthy', lastCheck: '2026-02-04T15:30:00', uptime: '99.99%' },
    { service: 'Message Queue', status: 'Healthy', lastCheck: '2026-02-04T15:30:00', uptime: '99.95%' },
    { service: 'API Gateway', status: 'Healthy', lastCheck: '2026-02-04T15:30:00', uptime: '99.97%' },
    { service: 'Cache Layer', status: 'Degraded', lastCheck: '2026-02-04T15:30:00', uptime: '99.85%' }
  ])

  function acknowledgeAlert(id) {
    const alert = alerts.value.find(a => a.id === id)
    if (alert) {
      alert.status = 'Acknowledged'
    }
  }

  function resolveAlert(id) {
    const alert = alerts.value.find(a => a.id === id)
    if (alert) {
      alert.status = 'Resolved'
    }
  }

  return {
    metrics,
    alerts,
    logs,
    traces,
    healthChecks,
    acknowledgeAlert,
    resolveAlert
  }
})
