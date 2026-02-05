# Simple PowerShell script to deploy STAR to AKS

$AcrName = "hspsdemo6478"
$Namespace = "star"

Write-Host "======================================" -ForegroundColor Green
Write-Host "STAR Pharmacy System Deployment" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Create namespace
Write-Host "`nCreating namespace..." -ForegroundColor Yellow
kubectl create namespace $Namespace 2>$null
kubectl label namespace $Namespace app=mckesson-star --overwrite

# Build images
Write-Host "`nBuilding Docker images in ACR..." -ForegroundColor Yellow
$acrLoginServer = az acr show --name $AcrName --query loginServer -o tsv

Write-Host "Building Security Portal..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-security-portal:1.0.0 --file ./security-portal/Dockerfile ./security-portal | Out-Null

Write-Host "Building Database Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-database-simulator:1.0.0 --file ./database-simulator/Dockerfile ./database-simulator | Out-Null

Write-Host "Building API Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-api-simulator:1.0.0 --file ./api-simulator/Dockerfile ./api-simulator | Out-Null

Write-Host "Building Web UI Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-webui-simulator:1.0.0 --file ./webui-simulator/Dockerfile ./webui-simulator | Out-Null

Write-Host "`nAll images built!" -ForegroundColor Green

# Deploy using kubectl with inline YAML
Write-Host "`nDeploying STAR applications..." -ForegroundColor Yellow

# ConfigMap and Secret
@"
apiVersion: v1
kind: ConfigMap
metadata:
  name: star-config
  namespace: $Namespace
data:
  SECURITY_PORTAL_URL: "http://security-portal.$Namespace.svc.cluster.local:8000"
  anomaly_frequency: "0.15"
  log_level: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: star-secrets
  namespace: $Namespace
type: Opaque
stringData:
  bearer_token: "star-secure-token-12345"
"@ | kubectl apply -f -

# Security Portal
@"
apiVersion: v1
kind: ServiceAccount
metadata:
  name: security-portal-sa
  namespace: $Namespace
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: security-portal
  namespace: $Namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: security-portal
  template:
    metadata:
      labels:
        app: security-portal
    spec:
      serviceAccountName: security-portal-sa
      containers:
      - name: security-portal
        image: $acrLoginServer/star-security-portal:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: APP_NAME
          value: "STAR Security Portal"
        - name: BEARER_TOKEN
          valueFrom:
            secretKeyRef:
              name: star-secrets
              key: bearer_token
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: security-portal
  namespace: $Namespace
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: security-portal
"@ | kubectl apply -f -

# Database Simulator
@"
apiVersion: v1
kind: ServiceAccount
metadata:
  name: star-database-sa
  namespace: $Namespace
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: star-database-simulator
  namespace: $Namespace
spec:
  replicas: 2
  selector:
    matchLabels:
      app: star-database-simulator
  template:
    metadata:
      labels:
        app: star-database-simulator
    spec:
      serviceAccountName: star-database-sa
      containers:
      - name: database-simulator
        image: $acrLoginServer/star-database-simulator:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: APP_NAME
          value: "STAR Pharmacy Database"
        - name: APP_TYPE
          value: "database"
        - name: SECURITY_PORTAL_URL
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: SECURITY_PORTAL_URL
        - name: BEARER_TOKEN
          valueFrom:
            secretKeyRef:
              name: star-secrets
              key: bearer_token
        - name: ANOMALY_FREQUENCY
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: anomaly_frequency
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: star-database-simulator
  namespace: $Namespace
spec:
  type: ClusterIP
  ports:
  - port: 8000
  selector:
    app: star-database-simulator
"@ | kubectl apply -f -

# API Simulator
@"
apiVersion: v1
kind: ServiceAccount
metadata:
  name: star-api-sa
  namespace: $Namespace
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: star-api-simulator
  namespace: $Namespace
spec:
  replicas: 3
  selector:
    matchLabels:
      app: star-api-simulator
  template:
    metadata:
      labels:
        app: star-api-simulator
    spec:
      serviceAccountName: star-api-sa
      containers:
      - name: api-simulator
        image: $acrLoginServer/star-api-simulator:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: APP_NAME
          value: "STAR Pharmacy API"
        - name: APP_TYPE
          value: "api"
        - name: SECURITY_PORTAL_URL
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: SECURITY_PORTAL_URL
        - name: BEARER_TOKEN
          valueFrom:
            secretKeyRef:
              name: star-secrets
              key: bearer_token
        - name: ANOMALY_FREQUENCY
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: anomaly_frequency
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: star-api-simulator
  namespace: $Namespace
spec:
  type: ClusterIP
  ports:
  - port: 8000
  selector:
    app: star-api-simulator
"@ | kubectl apply -f -

# Web UI Simulator
@"
apiVersion: v1
kind: ServiceAccount
metadata:
  name: star-webui-sa
  namespace: $Namespace
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: star-webui-simulator
  namespace: $Namespace
spec:
  replicas: 2
  selector:
    matchLabels:
      app: star-webui-simulator
  template:
    metadata:
      labels:
        app: star-webui-simulator
    spec:
      serviceAccountName: star-webui-sa
      containers:
      - name: webui-simulator
        image: $acrLoginServer/star-webui-simulator:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: APP_NAME
          value: "STAR Pharmacy Web UI"
        - name: APP_TYPE
          value: "webui"
        - name: SECURITY_PORTAL_URL
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: SECURITY_PORTAL_URL
        - name: BEARER_TOKEN
          valueFrom:
            secretKeyRef:
              name: star-secrets
              key: bearer_token
        - name: ANOMALY_FREQUENCY
          valueFrom:
            configMapKeyRef:
              name: star-config
              key: anomaly_frequency
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1"
---
apiVersion: v1
kind: Service
metadata:
  name: star-webui-simulator
  namespace: $Namespace
spec:
  type: ClusterIP
  ports:
  - port: 8000
  selector:
    app: star-webui-simulator
"@ | kubectl apply -f -

Write-Host "`nWaiting for pods..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "`n======================================" -ForegroundColor Green
Write-Host "STAR Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

kubectl get pods -n $Namespace
Write-Host ""
kubectl get services -n $Namespace

Write-Host "`nAccess STAR Security Portal:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n $Namespace svc/security-portal 8001:8000" -ForegroundColor Gray
Write-Host ""
