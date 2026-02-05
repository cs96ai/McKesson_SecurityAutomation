# PowerShell deployment script for Windows

Write-Host "======================================" -ForegroundColor Green
Write-Host "HSPS Kubernetes Deployment Script" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

Write-Host "Step 1: Creating namespace..." -ForegroundColor Yellow
kubectl apply -f kubernetes/namespace.yaml

Write-Host ""
Write-Host "Step 2: Creating shared ConfigMap and Secrets..." -ForegroundColor Yellow
kubectl apply -f database-simulator/kubernetes/configmap.yaml
kubectl apply -f database-simulator/kubernetes/secret.yaml

Write-Host ""
Write-Host "Step 3: Building Docker images..." -ForegroundColor Yellow
Write-Host "Building Security Portal..." -ForegroundColor Cyan
docker build -t security-portal:1.0.0 ./security-portal

Write-Host "Building Database Simulator..." -ForegroundColor Cyan
docker build -t hsps-database-simulator:1.0.0 ./database-simulator

Write-Host "Building API Simulator..." -ForegroundColor Cyan
docker build -t hsps-api-simulator:1.0.0 ./api-simulator

Write-Host "Building Web UI Simulator..." -ForegroundColor Cyan
docker build -t hsps-webui-simulator:1.0.0 ./webui-simulator

Write-Host ""
Write-Host "Step 4: Deploying Security Portal..." -ForegroundColor Yellow
kubectl apply -f security-portal/kubernetes/serviceaccount.yaml
kubectl apply -f security-portal/kubernetes/deployment.yaml
kubectl apply -f security-portal/kubernetes/service.yaml

Write-Host ""
Write-Host "Step 5: Waiting for Security Portal to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod -l app=security-portal -n hsps --timeout=120s

Write-Host ""
Write-Host "Step 6: Deploying Database Simulator..." -ForegroundColor Yellow
kubectl apply -f database-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f database-simulator/kubernetes/deployment.yaml
kubectl apply -f database-simulator/kubernetes/service.yaml

Write-Host ""
Write-Host "Step 7: Deploying API Simulator..." -ForegroundColor Yellow
kubectl apply -f api-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f api-simulator/kubernetes/deployment.yaml
kubectl apply -f api-simulator/kubernetes/service.yaml

Write-Host ""
Write-Host "Step 8: Deploying Web UI Simulator..." -ForegroundColor Yellow
kubectl apply -f webui-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f webui-simulator/kubernetes/deployment.yaml
kubectl apply -f webui-simulator/kubernetes/service.yaml

Write-Host ""
Write-Host "Step 9: Deploying Prometheus..." -ForegroundColor Yellow
kubectl apply -f monitoring/prometheus-config.yaml

Write-Host ""
Write-Host "Step 10: Deploying Grafana..." -ForegroundColor Yellow
kubectl apply -f monitoring/grafana-config.yaml

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Waiting for all pods to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod --all -n hsps --timeout=180s

Write-Host ""
Write-Host "Deployment Status:" -ForegroundColor Yellow
kubectl get pods -n hsps
Write-Host ""
kubectl get services -n hsps

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Access Information:" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "Security Portal Dashboard:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n hsps svc/security-portal 8000:8000"
Write-Host "  Then visit: http://localhost:8000"
Write-Host ""
Write-Host "Prometheus:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n hsps svc/prometheus 9090:9090"
Write-Host "  Then visit: http://localhost:9090"
Write-Host ""
Write-Host "Grafana:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n hsps svc/grafana 3000:3000"
Write-Host "  Then visit: http://localhost:3000"
Write-Host "  Username: admin, Password: admin"
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Cyan
Write-Host "  kubectl logs -f -n hsps -l app=security-portal"
Write-Host "  kubectl logs -f -n hsps -l app=hsps-database-simulator"
Write-Host "  kubectl logs -f -n hsps -l app=hsps-api-simulator"
Write-Host "  kubectl logs -f -n hsps -l app=hsps-webui-simulator"
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
