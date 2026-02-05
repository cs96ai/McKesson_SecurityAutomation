# PowerShell script to create an Azure Kubernetes Service (AKS) cluster
# Prerequisites: Azure CLI installed and logged in (az login)

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
    Write-Host "Please install Azure CLI from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Azure
Write-Host ""
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "Logged in as: $($account.user.name)" -ForegroundColor Green
    Write-Host "Subscription: $($account.name) ($($account.id))" -ForegroundColor Green
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

$confirmation = Read-Host "Do you want to proceed with cluster creation? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Cluster creation cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 1: Create Resource Group
Write-Host ""
Write-Host "Step 1: Creating Resource Group..." -ForegroundColor Yellow
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "true") {
    Write-Host "Resource Group '$ResourceGroupName' already exists" -ForegroundColor Green
} else {
    Write-Host "Creating Resource Group '$ResourceGroupName' in '$Location'..." -ForegroundColor Cyan
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
    Write-Host "AKS cluster '$ClusterName' already exists in resource group '$ResourceGroupName'" -ForegroundColor Red
    Write-Host "Please use a different cluster name or delete the existing cluster." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "Cluster name is available" -ForegroundColor Green
}

# Step 3: Create AKS Cluster
Write-Host ""
Write-Host "Step 3: Creating AKS Cluster..." -ForegroundColor Yellow
Write-Host "This may take 10-15 minutes. Please wait..." -ForegroundColor Cyan
Write-Host ""

az aks create `
    --resource-group $ResourceGroupName `
    --name $ClusterName `
    --location $Location `
    --node-count $NodeCount `
    --node-vm-size $NodeSize `
    --kubernetes-version $KubernetesVersion `
    --enable-managed-identity `
    --generate-ssh-keys `
    --network-plugin azure `
    --network-policy azure `
    --enable-addons monitoring `
    --output table

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "AKS Cluster created successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Failed to create AKS cluster" -ForegroundColor Red
    exit 1
}

# Step 4: Get AKS Credentials
Write-Host ""
Write-Host "Step 4: Getting AKS credentials..." -ForegroundColor Yellow
az aks get-credentials --resource-group $ResourceGroupName --name $ClusterName --overwrite-existing

if ($LASTEXITCODE -eq 0) {
    Write-Host "Credentials configured successfully" -ForegroundColor Green
} else {
    Write-Host "Failed to get credentials" -ForegroundColor Red
    exit 1
}

# Step 5: Verify cluster connection
Write-Host ""
Write-Host "Step 5: Verifying cluster connection..." -ForegroundColor Yellow
kubectl cluster-info

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Successfully connected to cluster" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Failed to connect to cluster" -ForegroundColor Red
    exit 1
}

# Step 6: Get cluster nodes
Write-Host ""
Write-Host "Step 6: Checking cluster nodes..." -ForegroundColor Yellow
kubectl get nodes

# Display cluster information
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "AKS Cluster Created Successfully!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Cluster Details:" -ForegroundColor Cyan
Write-Host "  Resource Group: $ResourceGroupName" -ForegroundColor White
Write-Host "  Cluster Name: $ClusterName" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Nodes: $NodeCount x $NodeSize" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Deploy HSPS applications:" -ForegroundColor White
Write-Host "     .\deploy-all.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. View cluster in Azure Portal:" -ForegroundColor White
Write-Host "     https://portal.azure.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Monitor cluster:" -ForegroundColor White
Write-Host "     kubectl get pods --all-namespaces" -ForegroundColor Gray
Write-Host "     kubectl top nodes" -ForegroundColor Gray
Write-Host ""
Write-Host "To delete the cluster later:" -ForegroundColor Yellow
Write-Host "  az aks delete --resource-group $ResourceGroupName --name $ClusterName --yes --no-wait" -ForegroundColor Gray
Write-Host "  az group delete --name $ResourceGroupName --yes --no-wait" -ForegroundColor Gray
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
