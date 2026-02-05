#!/bin/bash

set -e

echo "======================================"
echo "HSPS Kubernetes Deployment Script"
echo "======================================"
echo ""

echo "Step 1: Creating namespace..."
kubectl apply -f kubernetes/namespace.yaml

echo ""
echo "Step 2: Creating shared ConfigMap and Secrets..."
kubectl apply -f database-simulator/kubernetes/configmap.yaml
kubectl apply -f database-simulator/kubernetes/secret.yaml

echo ""
echo "Step 3: Building Docker images..."
echo "Building Security Portal..."
docker build -t security-portal:1.0.0 ./security-portal

echo "Building Database Simulator..."
docker build -t hsps-database-simulator:1.0.0 ./database-simulator

echo "Building API Simulator..."
docker build -t hsps-api-simulator:1.0.0 ./api-simulator

echo "Building Web UI Simulator..."
docker build -t hsps-webui-simulator:1.0.0 ./webui-simulator

echo ""
echo "Step 4: Deploying Security Portal..."
kubectl apply -f security-portal/kubernetes/serviceaccount.yaml
kubectl apply -f security-portal/kubernetes/deployment.yaml
kubectl apply -f security-portal/kubernetes/service.yaml

echo ""
echo "Step 5: Waiting for Security Portal to be ready..."
kubectl wait --for=condition=ready pod -l app=security-portal -n hsps --timeout=120s

echo ""
echo "Step 6: Deploying Database Simulator..."
kubectl apply -f database-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f database-simulator/kubernetes/deployment.yaml
kubectl apply -f database-simulator/kubernetes/service.yaml

echo ""
echo "Step 7: Deploying API Simulator..."
kubectl apply -f api-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f api-simulator/kubernetes/deployment.yaml
kubectl apply -f api-simulator/kubernetes/service.yaml

echo ""
echo "Step 8: Deploying Web UI Simulator..."
kubectl apply -f webui-simulator/kubernetes/serviceaccount.yaml
kubectl apply -f webui-simulator/kubernetes/deployment.yaml
kubectl apply -f webui-simulator/kubernetes/service.yaml

echo ""
echo "Step 9: Deploying Prometheus..."
kubectl apply -f monitoring/prometheus-config.yaml

echo ""
echo "Step 10: Deploying Grafana..."
kubectl apply -f monitoring/grafana-config.yaml

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Waiting for all pods to be ready..."
kubectl wait --for=condition=ready pod --all -n hsps --timeout=180s

echo ""
echo "Deployment Status:"
kubectl get pods -n hsps
echo ""
kubectl get services -n hsps

echo ""
echo "======================================"
echo "Access Information:"
echo "======================================"
echo "Security Portal Dashboard:"
echo "  kubectl port-forward -n hsps svc/security-portal 8000:8000"
echo "  Then visit: http://localhost:8000"
echo ""
echo "Prometheus:"
echo "  kubectl port-forward -n hsps svc/prometheus 9090:9090"
echo "  Then visit: http://localhost:9090"
echo ""
echo "Grafana:"
echo "  kubectl port-forward -n hsps svc/grafana 3000:3000"
echo "  Then visit: http://localhost:3000"
echo "  Username: admin, Password: admin"
echo ""
echo "To view logs:"
echo "  kubectl logs -f -n hsps -l app=security-portal"
echo "  kubectl logs -f -n hsps -l app=hsps-database-simulator"
echo "  kubectl logs -f -n hsps -l app=hsps-api-simulator"
echo "  kubectl logs -f -n hsps -l app=hsps-webui-simulator"
echo ""
echo "======================================"
