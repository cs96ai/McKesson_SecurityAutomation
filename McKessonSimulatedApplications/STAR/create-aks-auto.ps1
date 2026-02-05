# PowerShell script to create an Azure Kubernetes Service (AKS) cluster
# Auto-confirm version for automation

param(
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroupName = "hsps-demo-rg",
    
    [Parameter(Mandatory=$false)]
    [string]$ClusterName = "hsps-aks-cluster",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$false)]
    [int]$NodeCount = 3,
    
    [Parameter(Mandatory=$false)]
    [string]$NodeSize = "Standard_B2s",
    
    [Parameter(Mandatory=$false)]
    [string]$KubernetesVersion = "1.28.3"
)

Write-Host "======================================" -ForegroundColor Green
Write-Host "Azure AKS Cluster Creation Script" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Check if Azure CLI is installed
Write-Host "Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "Azure CLI is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if logged in to Azure
Write-Host ""
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "Subscription: $($account.name)" -ForegroundColor Green
} catch {
    Write-Host "Not logged in to Azure" -ForegroundColor Red
    Write-Host "Please run: az login" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Cluster Configuration:" -ForegroundColor Cyan
Write-Host "  Resource Group: $ResourceGroupName" -ForegroundColor White
Write-Host "  Cluster Name: $ClusterName" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Node Count: $NodeCount" -ForegroundColor White
Write-Host "  Node Size: $NodeSize" -ForegroundColor White
Write-Host "  Kubernetes Version: $KubernetesVersion" -ForegroundColor White
Write-Host ""

# Step 1: Create Resource Group
Write-Host "Step 1: Creating Resource Group..." -ForegroundColor Yellow
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "true") {
    Write-Host "Resource Group '$ResourceGroupName' already exists" -ForegroundColor Green
} else {
    Write-Host "Creating Resource Group..." -ForegroundColor Cyan
    az group create --name $ResourceGroupName --location $Location --output table
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Resource Group created successfully" -ForegroundColor Green
    } else {
        Write-Host "Failed to create Resource Group" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Check if cluster already exists
Write-Host ""
Write-Host "Step 2: Checking if AKS cluster exists..." -ForegroundColor Yellow
$clusterExists = az aks show --resource-group $ResourceGroupName --name $ClusterName --output json 2>$null
if ($clusterExists) {
    Write-Host "AKS cluster '$ClusterName' already exists" -ForegroundColor Yellow
    Write-Host "Skipping cluster creation, getting credentials..." -ForegroundColor Cyan
    az aks get-credentials --resource-group $ResourceGroupName --name $ClusterName --overwrite-existing
    kubectl get nodes
    Write-Host ""
    Write-Host "Cluster is ready for deployment!" -ForegroundColor Green
    exit 0
}

Write-Host "Cluster name is available" -ForegroundColor Green

# Step 3: Create AKS Cluster
Write-Host ""
Write-Host "Step 3: Creating AKS Cluster..." -ForegroundColor Yellow
Write-Host "This will take 10-15 minutes. Please wait..." -ForegroundColor Cyan
Write-Host ""

az aks create `
    --resource-group $ResourceGroupName `
    --name $ClusterName `
    --location $Location `
    --node-count $NodeCount `
    --node-vm-size $NodeSize `
    --enable-managed-identity `
    --generate-ssh-keys `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Failed to create AKS cluster" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "AKS Cluster created successfully!" -ForegroundColor Green

# Step 4: Get AKS Credentials
Write-Host ""
Write-Host "Step 4: Getting AKS credentials..." -ForegroundColor Yellow
az aks get-credentials --resource-group $ResourceGroupName --name $ClusterName --overwrite-existing

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to get credentials" -ForegroundColor Red
    exit 1
}

Write-Host "Credentials configured successfully" -ForegroundColor Green

# Step 5: Verify cluster
Write-Host ""
Write-Host "Step 5: Verifying cluster..." -ForegroundColor Yellow
kubectl get nodes

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "AKS Cluster Ready!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Deploy HSPS applications with .\deploy-all.ps1" -ForegroundColor Cyan
Write-Host ""
