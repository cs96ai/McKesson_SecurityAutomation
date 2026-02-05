# PowerShell script to deploy STAR Pharmacy Management System to AKS

param(
    [Parameter(Mandatory=$false)]
    [string]$AcrName = "hspsdemo6478",
    
    [Parameter(Mandatory=$false)]
    [string]$Namespace = "star"
)

Write-Host "======================================" -ForegroundColor Green
Write-Host "STAR Pharmacy System Deployment" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Step 1: Create namespace
Write-Host "Step 1: Creating namespace '$Namespace'..." -ForegroundColor Yellow
kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -
kubectl label namespace $Namespace app=mckesson-star system=pharmacy --overwrite

# Step 2: Build Docker images in ACR
Write-Host ""
Write-Host "Step 2: Building STAR Docker images in ACR..." -ForegroundColor Yellow

Write-Host "Building STAR Security Portal..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-security-portal:1.0.0 --file ./security-portal/Dockerfile ./security-portal

Write-Host "Building STAR Database Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-database-simulator:1.0.0 --file ./database-simulator/Dockerfile ./database-simulator

Write-Host "Building STAR API Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-api-simulator:1.0.0 --file ./api-simulator/Dockerfile ./api-simulator

Write-Host "Building STAR Web UI Simulator..." -ForegroundColor Cyan
az acr build --registry $AcrName --image star-webui-simulator:1.0.0 --file ./webui-simulator/Dockerfile ./webui-simulator

Write-Host ""
Write-Host "All STAR images built successfully!" -ForegroundColor Green

# Step 3: Get ACR login server
$acrLoginServer = az acr show --name $AcrName --query loginServer -o tsv

# Step 4: Create ConfigMap
Write-Host ""
Write-Host "Step 3: Creating ConfigMap and Secrets..." -ForegroundColor Yellow

kubectl apply -f - <<EOF
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
  bearer_token: "star-secure-token-change-in-production-12345"
EOF

# Step 5: Deploy Security Portal
Write-Host ""
Write-Host "Step 4: Deploying STAR Security Portal..." -ForegroundColor Yellow

kubectl apply -f - <<EOF
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
  labels:
    app: security-portal
    system: mckesson-star
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
        imagePullPolicy: Always
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
EOF

# Step 6: Deploy Database Simulator
Write-Host ""
Write-Host "Step 5: Deploying STAR Database Simulator..." -ForegroundColor Yellow

kubectl apply -f - <<EOF
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
  labels:
    app: star-database-simulator
    system: mckesson-star
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
        imagePullPolicy: Always
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
    targetPort: 8000
  selector:
    app: star-database-simulator
EOF

# Step 7: Deploy API Simulator
Write-Host ""
Write-Host "Step 6: Deploying STAR API Simulator..." -ForegroundColor Yellow

kubectl apply -f - <<EOF
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
  labels:
    app: star-api-simulator
    system: mckesson-star
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
        imagePullPolicy: Always
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
    targetPort: 8000
  selector:
    app: star-api-simulator
EOF

# Step 8: Deploy Web UI Simulator
Write-Host ""
Write-Host "Step 7: Deploying STAR Web UI Simulator..." -ForegroundColor Yellow

kubectl apply -f - <<EOF
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
  labels:
    app: star-webui-simulator
    system: mckesson-star
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
        imagePullPolicy: Always
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
    targetPort: 8000
  selector:
    app: star-webui-simulator
EOF

# Step 9: Wait for deployments
Write-Host ""
Write-Host "Step 8: Waiting for deployments to be ready..." -ForegroundColor Yellow
kubectl wait --for=condition=ready pod --all -n $Namespace --timeout=300s

# Step 10: Display status
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "STAR Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

kubectl get pods -n $Namespace
Write-Host ""
kubectl get services -n $Namespace

Write-Host ""
Write-Host "Access STAR Security Portal:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n $Namespace svc/security-portal 8001:8000" -ForegroundColor Gray
Write-Host "  Then visit: http://localhost:8001" -ForegroundColor Gray
Write-Host ""
Write-Host "STAR Pharmacy Management System is now running!" -ForegroundColor Green
Write-Host ""
