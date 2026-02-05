# Auto-Shutdown Kubernetes Pods After 15 Minutes
# This script monitors pod lifecycle and automatically stops pods after 15 minutes to save costs
# Can be run as an Azure Function with Timer Trigger or as a scheduled task

param(
    [string]$ResourceGroup = "hsps-demo",
    [string]$ClusterName = "hsps-aks-cluster",
    [int]$TimeoutMinutes = 15
)

Write-Host "=== Kubernetes Pod Auto-Shutdown Script ===" -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Cluster Name: $ClusterName"
Write-Host "Timeout: $TimeoutMinutes minutes"
Write-Host ""

# Connect to AKS cluster
Write-Host "Connecting to AKS cluster..." -ForegroundColor Yellow
az aks get-credentials --resource-group $ResourceGroup --name $ClusterName --overwrite-existing

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to connect to AKS cluster" -ForegroundColor Red
    exit 1
}

# Function to get pod creation time
function Get-PodAge {
    param([string]$Namespace, [string]$PodName)
    
    $creationTime = kubectl get pod $PodName -n $Namespace -o jsonpath='{.metadata.creationTimestamp}'
    if ($creationTime) {
        $created = [DateTime]::Parse($creationTime)
        $age = (Get-Date).ToUniversalTime() - $created
        return $age.TotalMinutes
    }
    return 0
}

# Function to scale down deployment
function Stop-Deployment {
    param([string]$Namespace, [string]$DeploymentName)
    
    Write-Host "  Scaling down deployment: $Namespace/$DeploymentName" -ForegroundColor Yellow
    kubectl scale deployment $DeploymentName -n $Namespace --replicas=0
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Successfully scaled down $DeploymentName" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  ✗ Failed to scale down $DeploymentName" -ForegroundColor Red
        return $false
    }
}

# Check HSPS namespace
Write-Host "`nChecking HSPS namespace..." -ForegroundColor Cyan
$hspsDeployments = @(
    "hsps-database-simulator",
    "hsps-api-simulator",
    "hsps-webui-simulator",
    "security-portal"
)

foreach ($deployment in $hspsDeployments) {
    $pods = kubectl get pods -n hsps -l app=$deployment -o jsonpath='{.items[*].metadata.name}'
    
    if ($pods) {
        $podList = $pods -split ' '
        foreach ($pod in $podList) {
            if ($pod) {
                $ageMinutes = Get-PodAge -Namespace "hsps" -PodName $pod
                Write-Host "  Pod: $pod - Age: $([math]::Round($ageMinutes, 2)) minutes"
                
                if ($ageMinutes -ge $TimeoutMinutes) {
                    Write-Host "  ⚠ Pod has exceeded timeout threshold!" -ForegroundColor Red
                    Stop-Deployment -Namespace "hsps" -DeploymentName $deployment
                    break
                }
            }
        }
    } else {
        Write-Host "  No pods found for deployment: $deployment" -ForegroundColor Gray
    }
}

# Check STAR namespace
Write-Host "`nChecking STAR namespace..." -ForegroundColor Cyan
$starDeployments = @(
    "star-database-simulator",
    "star-api-simulator",
    "star-webui-simulator",
    "security-portal"
)

foreach ($deployment in $starDeployments) {
    $pods = kubectl get pods -n star -l app=$deployment -o jsonpath='{.items[*].metadata.name}'
    
    if ($pods) {
        $podList = $pods -split ' '
        foreach ($pod in $podList) {
            if ($pod) {
                $ageMinutes = Get-PodAge -Namespace "star" -PodName $pod
                Write-Host "  Pod: $pod - Age: $([math]::Round($ageMinutes, 2)) minutes"
                
                if ($ageMinutes -ge $TimeoutMinutes) {
                    Write-Host "  ⚠ Pod has exceeded timeout threshold!" -ForegroundColor Red
                    Stop-Deployment -Namespace "star" -DeploymentName $deployment
                    break
                }
            }
        }
    } else {
        Write-Host "  No pods found for deployment: $deployment" -ForegroundColor Gray
    }
}

# Optional: Stop other Azure resources to save costs
Write-Host "`nChecking for other running resources..." -ForegroundColor Cyan

# Check if any pods are still running
$hspsPods = kubectl get pods -n hsps --no-headers 2>$null | Measure-Object | Select-Object -ExpandProperty Count
$starPods = kubectl get pods -n star --no-headers 2>$null | Measure-Object | Select-Object -ExpandProperty Count

if ($hspsPods -eq 0 -and $starPods -eq 0) {
    Write-Host "`n✓ All application pods have been stopped" -ForegroundColor Green
    Write-Host "  HSPS pods: 0" -ForegroundColor Gray
    Write-Host "  STAR pods: 0" -ForegroundColor Gray
    
    # Optional: You could also stop the AKS cluster here to save more costs
    # Uncomment the following lines if you want to stop the entire cluster
    # Write-Host "`nStopping AKS cluster to save costs..." -ForegroundColor Yellow
    # az aks stop --resource-group $ResourceGroup --name $ClusterName
} else {
    Write-Host "`nSome pods are still running:" -ForegroundColor Yellow
    Write-Host "  HSPS pods: $hspsPods" -ForegroundColor Gray
    Write-Host "  STAR pods: $starPods" -ForegroundColor Gray
}

Write-Host "`n=== Auto-Shutdown Check Complete ===" -ForegroundColor Cyan
Write-Host "Next check will run based on your schedule (recommended: every 5 minutes)" -ForegroundColor Gray
