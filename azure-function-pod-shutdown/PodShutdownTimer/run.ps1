# Azure Function Timer Trigger - Auto-Shutdown Kubernetes Pods After 15 Minutes
# Runs every 5 minutes to check pod ages and scale down deployments

param($Timer)

$ResourceGroup = "hsps-demo-rg"
$ClusterName = "hsps-aks-cluster"
$TimeoutMinutes = 15

Write-Host "=== Kubernetes Pod Auto-Shutdown Function ===" -ForegroundColor Cyan
Write-Host "Execution Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Resource Group: $ResourceGroup"
Write-Host "Cluster Name: $ClusterName"
Write-Host "Timeout: $TimeoutMinutes minutes"
Write-Host ""

try {
    # Connect to AKS cluster using managed identity
    Write-Host "Connecting to AKS cluster..." -ForegroundColor Yellow
    az aks get-credentials --resource-group $ResourceGroup --name $ClusterName --overwrite-existing --admin
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to connect to AKS cluster" -ForegroundColor Red
        throw "AKS connection failed"
    }

    # Function to get pod creation time
    function Get-PodAge {
        param([string]$Namespace, [string]$PodName)
        
        $creationTime = kubectl get pod $PodName -n $Namespace -o jsonpath='{.metadata.creationTimestamp}' 2>$null
        if ($creationTime) {
            try {
                $created = [DateTime]::Parse($creationTime)
                $age = (Get-Date).ToUniversalTime() - $created
                return $age.TotalMinutes
            } catch {
                Write-Host "  Warning: Could not parse creation time for $PodName" -ForegroundColor Yellow
                return 0
            }
        }
        return 0
    }

    # Function to scale down deployment
    function Stop-Deployment {
        param([string]$Namespace, [string]$DeploymentName)
        
        Write-Host "  ⚠ Scaling down deployment: $Namespace/$DeploymentName" -ForegroundColor Yellow
        kubectl scale deployment $DeploymentName -n $Namespace --replicas=0 2>$null
        
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

    $shutdownCount = 0
    foreach ($deployment in $hspsDeployments) {
        $pods = kubectl get pods -n hsps -l app=$deployment -o jsonpath='{.items[*].metadata.name}' 2>$null
        
        if ($pods -and $pods.Trim()) {
            $podList = $pods -split ' '
            foreach ($pod in $podList) {
                if ($pod.Trim()) {
                    $ageMinutes = Get-PodAge -Namespace "hsps" -PodName $pod
                    Write-Host "  Pod: $pod - Age: $([math]::Round($ageMinutes, 2)) minutes"
                    
                    if ($ageMinutes -ge $TimeoutMinutes) {
                        Write-Host "  ⚠ Pod has exceeded timeout threshold ($TimeoutMinutes min)!" -ForegroundColor Red
                        if (Stop-Deployment -Namespace "hsps" -DeploymentName $deployment) {
                            $shutdownCount++
                        }
                        break
                    }
                }
            }
        } else {
            Write-Host "  No pods running for: $deployment" -ForegroundColor Gray
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
        $pods = kubectl get pods -n star -l app=$deployment -o jsonpath='{.items[*].metadata.name}' 2>$null
        
        if ($pods -and $pods.Trim()) {
            $podList = $pods -split ' '
            foreach ($pod in $podList) {
                if ($pod.Trim()) {
                    $ageMinutes = Get-PodAge -Namespace "star" -PodName $pod
                    Write-Host "  Pod: $pod - Age: $([math]::Round($ageMinutes, 2)) minutes"
                    
                    if ($ageMinutes -ge $TimeoutMinutes) {
                        Write-Host "  ⚠ Pod has exceeded timeout threshold ($TimeoutMinutes min)!" -ForegroundColor Red
                        if (Stop-Deployment -Namespace "star" -DeploymentName $deployment) {
                            $shutdownCount++
                        }
                        break
                    }
                }
            }
        } else {
            Write-Host "  No pods running for: $deployment" -ForegroundColor Gray
        }
    }

    # Summary
    Write-Host "`n=== Summary ===" -ForegroundColor Cyan
    $hspsPods = kubectl get pods -n hsps --no-headers 2>$null | Measure-Object | Select-Object -ExpandProperty Count
    $starPods = kubectl get pods -n star --no-headers 2>$null | Measure-Object | Select-Object -ExpandProperty Count
    
    Write-Host "Deployments scaled down: $shutdownCount"
    Write-Host "Current HSPS pods: $hspsPods"
    Write-Host "Current STAR pods: $starPods"
    
    if ($hspsPods -eq 0 -and $starPods -eq 0) {
        Write-Host "`n✓ All application pods have been stopped - Cost savings active!" -ForegroundColor Green
    }

} catch {
    Write-Host "`n✗ Error during execution: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace
    throw
}

Write-Host "`n=== Auto-Shutdown Check Complete ===" -ForegroundColor Cyan
Write-Host "Next execution in 5 minutes"
