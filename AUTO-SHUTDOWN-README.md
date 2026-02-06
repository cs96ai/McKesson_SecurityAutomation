# Kubernetes Pod Auto-Shutdown

This script automatically stops Kubernetes pods after 15 minutes for resource management.

## Overview

The `auto-shutdown-pods.ps1` script monitors all pods in the HSPS and STAR namespaces and automatically scales down deployments when pods have been running for more than 15 minutes.

## Usage

### Manual Execution

Run the script manually to check and stop pods:

```powershell
.\auto-shutdown-pods.ps1
```

With custom parameters:

```powershell
.\auto-shutdown-pods.ps1 -ResourceGroup "hsps-demo" -ClusterName "hsps-aks-cluster" -TimeoutMinutes 15
```

### Automated Execution Options

#### Option 1: Windows Task Scheduler (Recommended for Local Development)

1. Open Task Scheduler
2. Create a new task
3. Set trigger to run every 5 minutes
4. Set action to run PowerShell with the script path
5. Configure to run whether user is logged in or not

#### Option 2: Azure Automation Runbook (Recommended for Production)

1. Create an Azure Automation Account
2. Import the PowerShell script as a Runbook
3. Create a schedule to run every 5 minutes
4. Link the schedule to the runbook

#### Option 3: Azure Function with Timer Trigger

1. Create an Azure Function App
2. Create a Timer Trigger function (cron: `0 */5 * * * *` for every 5 minutes)
3. Use the PowerShell script logic in the function
4. Deploy to Azure

## What It Does

1. **Connects to AKS** - Authenticates with your Azure Kubernetes cluster
2. **Checks Pod Ages** - Calculates how long each pod has been running
3. **Scales Down Deployments** - If a pod exceeds 15 minutes, scales the deployment to 0 replicas
4. **Reports Status** - Provides detailed output of actions taken

## Monitored Deployments

### HSPS Namespace
- hsps-database-simulator
- hsps-api-simulator
- hsps-webui-simulator
- security-portal

### STAR Namespace
- star-database-simulator
- star-api-simulator
- star-webui-simulator
- security-portal

## Benefits

By automatically stopping pods after 15 minutes:
- **Resource Management**: Pods only run during active demos
- **Storage**: Persistent volumes remain available
- **Network**: Reduced egress traffic

## Prerequisites

- Azure CLI installed and configured
- kubectl installed and configured
- PowerShell 5.1 or higher
- Appropriate permissions to manage AKS cluster

## Customization

### Change Timeout Duration

```powershell
.\auto-shutdown-pods.ps1 -TimeoutMinutes 30  # 30 minutes 
```

### Add Additional Namespaces

Edit the script and add new namespace checks similar to HSPS and STAR sections.

### Stop Entire AKS Cluster

Uncomment the lines at the end of the script to stop the entire AKS cluster when all pods are down:

```powershell
# az aks stop --resource-group $ResourceGroup --name $ClusterName
```

## Monitoring

The script outputs detailed logs showing:
- Pod names and ages
- Which deployments were scaled down
- Current pod counts in each namespace

## Troubleshooting

### Script fails to connect to AKS
- Ensure you're logged in to Azure: `az login`
- Verify cluster name and resource group are correct
- Check you have appropriate RBAC permissions

### Pods not scaling down
- Verify the deployment names match exactly
- Check kubectl access: `kubectl get pods -n hsps`
- Ensure you have permissions to scale deployments

## Integration with Vue SPA

The Vue SPA's Kubernetes Monitor page attempts to notify the backend when pods start via:

```javascript
POST /api/pod-lifecycle/start
```

This can be used to track exact start times if you implement a backend service.

## Best Practices

1. **Run frequently**: Schedule every 5 minutes to catch pods quickly
2. **Monitor logs**: Review execution logs to ensure proper operation
3. **Test first**: Run manually before scheduling
4. **Adjust timeout**: 15 minutes is default, adjust based on your demo needs
5. **Alert on failures**: Set up alerts if the script fails to run

## Example Output

```
=== Kubernetes Pod Auto-Shutdown Script ===
Resource Group: hsps-demo
Cluster Name: hsps-aks-cluster
Timeout: 15 minutes

Connecting to AKS cluster...

Checking HSPS namespace...
  Pod: hsps-database-simulator-abc123 - Age: 16.5 minutes
  ⚠ Pod has exceeded timeout threshold!
  Scaling down deployment: hsps/hsps-database-simulator
  ✓ Successfully scaled down hsps-database-simulator

Checking STAR namespace...
  Pod: star-api-simulator-xyz789 - Age: 12.3 minutes
  No pods found for deployment: star-webui-simulator

✓ All application pods have been stopped
  HSPS pods: 0
  STAR pods: 0

=== Auto-Shutdown Check Complete ===
```
