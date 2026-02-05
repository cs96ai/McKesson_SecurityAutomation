# PowerShell script to create ACR, build images, and deploy to AKS

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "hsps-demo-rg",
    
    [Parameter(Mandatory=$false)]
    [string]$AcrName = "hspsdemo$(Get-Random -Minimum 1000 -Maximum 9999)",
    
    [Parameter(Mandatory=$false)]
    [string]$ClusterName = "hsps-aks-cluster"
)

Write-Host "======================================" -ForegroundColor Green
Write-Host "HSPS ACR Setup and Deployment" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Step 1: Create Azure Container Registry
Write-Host "Step 1: Creating Azure Container Registry..." -ForegroundColor Yellow
$acrExists = az acr show --name $AcrName --resource-group $ResourceGroupName 2>$null
if ($acrExists) {
    Write-Host "ACR '$AcrName' already exists" -ForegroundColor Green
} else {
    Write-Host "Creating ACR '$AcrName'..." -ForegroundColor Cyan
    az acr create --resource-group $ResourceGroupName --name $AcrName --sku Basic --output table
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create ACR" -ForegroundColor Red
        exit 1
    }
    Write-Host "ACR created successfully" -ForegroundColor Green
}

# Step 2: Attach ACR to AKS
Write-Host ""
Write-Host "Step 2: Attaching ACR to AKS cluster..." -ForegroundColor Yellow
az aks update --resource-group $ResourceGroupName --name $ClusterName --attach-acr $AcrName
if ($LASTEXITCODE -eq 0) {
    Write-Host "ACR attached to AKS successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to attach ACR to AKS" -ForegroundColor Red
    exit 1
}

# Step 3: Build images using ACR
Write-Host ""
Write-Host "Step 3: Building Docker images in ACR..." -ForegroundColor Yellow

Write-Host "Building Security Portal..." -ForegroundColor Cyan
az acr build --registry $AcrName --image security-portal:1.0.0 --file ./security-portal/Dockerfile ./security-portal

Write-Host "Building Database Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image hsps-database-simulator:1.0.0 --file ./database-simulator/Dockerfile ./database-simulator

Write-Host "Building API Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image hsps-api-simulator:1.0.0 --file ./api-simulator/Dockerfile ./api-simulator

Write-Host "Building Web UI Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image hsps-webui-simulator:1.0.0 --file ./webui-simulator/Dockerfile ./webui-simulator

Write-Host ""
Write-Host "All images built successfully!" -ForegroundColor Green

# Step 4: Update Kubernetes manifests with ACR name
Write-Host ""
Write-Host "Step 4: Updating Kubernetes manifests..." -ForegroundColor Yellow
$acrLoginServer = az acr show --name $AcrName --query loginServer -o tsv

# Update deployment files
$files = @(
    "security-portal/kubernetes/deployment.yaml",
    "database-simulator/kubernetes/deployment.yaml",
    "api-simulator/kubernetes/deployment.yaml",
    "webui-simulator/kubernetes/deployment.yaml"
)

foreach ($file in $files) {
    $content = Get-Content $file -Raw
    $content = $content -replace "image: security-portal:1.0.0", "image: $acrLoginServer/security-portal:1.0.0"
    $content = $content -replace "image: hsps-database-simulator:1.0.0", "image: $acrLoginServer/hsps-database-simulator:1.0.0"
    $content = $content -replace "image: hsps-api-simulator:1.0.0", "image: $acrLoginServer/hsps-api-simulator:1.0.0"
    $content = $content -replace "image: hsps-webui-simulator:1.0.0", "image: $acrLoginServer/hsps-webui-simulator:1.0.0"
    $content = $content -replace "imagePullPolicy: IfNotPresent", "imagePullPolicy: Always"
    Set-Content $file -Value $content
}

Write-Host "Manifests updated with ACR registry: $acrLoginServer" -ForegroundColor Green

# Step 5: Deploy to Kubernetes
Write-Host ""
Write-Host "Step 5: Deploying to Kubernetes..." -ForegroundColor Yellow

Write-Host "Creating namespace..." -ForegroundColor Cyan
kubectl apply -f kubernetes/namespace.yaml

Write-Host "Creating ConfigMap and Secrets..." -ForegroundColor Cyan
kubectl apply -f database-simulator/kubernetes/configmap.yaml
kubectl apply -f database-simulator/kubernetes/secret.yaml

Write-Host "Deploying Security Portal..." -ForegroundColor Cyan
kubectl apply -f security-portal/kubernetes/serviceaccount.yaml
kubectl apply -f security-portal/kubernetes/deployment.yaml
kubectl apply -f security-portal/kubernetes/service.yaml

Write-Host "Deploying Database Simulator..." -ForegroundColor Cyan
kubectl apply -f database-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f database-simulator/kubernetes/deployment.yaml
kubectl apply -f database-simulator/kubernetes/service.yaml

Write-Host "Deploying API Simulator..." -ForegroundColor Cyan
kubectl apply -f api-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f api-simulator/kubernetes/deployment.yaml
kubectl apply -f api-simulator/kubernetes/service.yaml

Write-Host "Deploying Web UI Simulator..." -ForegroundColor Cyan
kubectl apply -f webui-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f webui-simulator/kubernetes/deployment.yaml
kubectl apply -f webui-simulator/kubernetes/service.yaml

Write-Host "Deploying Prometheus..." -ForegroundColor Cyan
kubectl apply -f monitoring/prometheus-config.yaml

Write-Host "Deploying Grafana..." -ForegroundColor Cyan
kubectl apply -f monitoring/grafana-config.yaml

Write-Host ""
Write-Host "Waiting for pods to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod --all -n hsps --timeout=300s

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

kubectl get pods -n hsps
Write-Host ""
kubectl get services -n hsps

Write-Host ""
Write-Host "Access Applications:" -ForegroundColor Cyan
Write-Host "  Security Portal:" -ForegroundColor White
Write-Host "    kubectl port-forward -n hsps svc/security-portal 8000:8000" -ForegroundColor Gray
Write-Host "    Then visit: http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "  Prometheus:" -ForegroundColor White
Write-Host "    kubectl port-forward -n hsps svc/prometheus 9090:9090" -ForegroundColor Gray
Write-Host ""
Write-Host "  Grafana:" -ForegroundColor White
Write-Host "    kubectl port-forward -n hsps svc/grafana 3000:3000" -ForegroundColor Gray
Write-Host "    Username: admin, Password: admin" -ForegroundColor Gray
Write-Host ""
