"""
Unit tests for FastAPI Azure Backend
Tests all 15 Azure read-only API endpoints
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

BEARER_TOKEN = "your-secret-token-123"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

@pytest.fixture
def client():
    """Create test client"""
    from starlette.testclient import TestClient
    from main import app
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_azure_credentials():
    """Mock Azure credentials and clients"""
    with patch.dict(os.environ, {
        'VITE_AZURE_TENANT_ID': '33b0dd0d-0cdb-43e3-885b-68259cb8efef',
        'VITE_AZURE_CLIENT_ID': '85336049-1660-4b67-8ddf-0ba4e50e914b',
        'VITE_AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_SUBSCRIPTION_ID': '3306e559-a033-43dd-bf98-fc59174d563f',
        'VITE_BEARER_TOKEN': BEARER_TOKEN
    }):
        yield

def test_health_endpoint(client):
    """Test 1: Health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_unauthorized_access(client):
    """Test 2: Verify bearer token authentication"""
    response = client.get("/api/azure/aks/status")
    assert response.status_code == 403
    assert "Invalid or missing bearer token" in response.json()["detail"]

@patch('main.ContainerServiceClient')
def test_aks_status(mock_container_client, mock_azure_credentials, client):
    """Test 3: AKS cluster status endpoint"""
    mock_cluster = Mock()
    mock_cluster.name = "test-cluster"
    mock_cluster.location = "eastus"
    mock_cluster.power_state.code = "Running"
    mock_cluster.provisioning_state = "Succeeded"
    mock_cluster.kubernetes_version = "1.28.0"
    mock_cluster.node_resource_group = "test-rg"
    mock_cluster.fqdn = "test.hcp.eastus.azmk8s.io"
    
    mock_profile = Mock()
    mock_profile.name = "nodepool1"
    mock_profile.count = 3
    mock_profile.vm_size = "Standard_DS2_v2"
    mock_profile.os_type = "Linux"
    mock_cluster.agent_pool_profiles = [mock_profile]
    
    mock_client_instance = Mock()
    mock_client_instance.managed_clusters.get.return_value = mock_cluster
    mock_container_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/aks/status", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-cluster"
    assert data["powerState"] == "Running"

@patch('main.client.CoreV1Api')
@patch('main.config.load_kube_config_from_dict')
def test_aks_pods(mock_load_config, mock_core_api, mock_azure_credentials):
    """Test 4: AKS pods list endpoint"""
    mock_pod = Mock()
    mock_pod.metadata.name = "test-pod"
    mock_pod.metadata.namespace = "default"
    mock_pod.status.phase = "Running"
    mock_pod.spec.node_name = "node-1"
    
    mock_container = Mock()
    mock_container.name = "app"
    mock_container.image = "nginx:latest"
    mock_pod.spec.containers = [mock_container]
    
    mock_pod_list = Mock()
    mock_pod_list.items = [mock_pod]
    
    mock_api_instance = Mock()
    mock_api_instance.list_pod_for_all_namespaces.return_value = mock_pod_list
    mock_core_api.return_value = mock_api_instance
    
    response = client.get("/api/azure/aks/pods", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["pods"]) > 0

@patch('main.client.AppsV1Api')
@patch('main.config.load_kube_config_from_dict')
def test_aks_deployments(mock_load_config, mock_apps_api, mock_azure_credentials):
    """Test 5: AKS deployments list endpoint"""
    mock_deployment = Mock()
    mock_deployment.metadata.name = "test-deployment"
    mock_deployment.metadata.namespace = "default"
    mock_deployment.spec.replicas = 3
    mock_deployment.status.ready_replicas = 3
    mock_deployment.status.available_replicas = 3
    
    mock_deployment_list = Mock()
    mock_deployment_list.items = [mock_deployment]
    
    mock_api_instance = Mock()
    mock_api_instance.list_deployment_for_all_namespaces.return_value = mock_deployment_list
    mock_apps_api.return_value = mock_api_instance
    
    response = client.get("/api/azure/aks/deployments", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["deployments"]) > 0

@patch('main.ResourceManagementClient')
def test_resource_groups(mock_resource_client, mock_azure_credentials):
    """Test 6: Resource groups list endpoint"""
    mock_rg = Mock()
    mock_rg.name = "test-rg"
    mock_rg.location = "eastus"
    mock_rg.tags = {"env": "test"}
    
    mock_client_instance = Mock()
    mock_client_instance.resource_groups.list.return_value = [mock_rg]
    mock_resource_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/resource-groups", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["resourceGroups"]) > 0

@patch('main.ResourceManagementClient')
def test_resources_by_group(mock_resource_client, mock_azure_credentials):
    """Test 7: Resources by group endpoint"""
    mock_resource = Mock()
    mock_resource.name = "test-resource"
    mock_resource.type = "Microsoft.Compute/virtualMachines"
    mock_resource.location = "eastus"
    
    mock_client_instance = Mock()
    mock_client_instance.resources.list_by_resource_group.return_value = [mock_resource]
    mock_resource_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/resources/test-rg", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["resourceGroup"] == "test-rg"

@patch('main.WebSiteManagementClient')
def test_app_services(mock_web_client, mock_azure_credentials):
    """Test 8: App Services list endpoint"""
    mock_app = Mock()
    mock_app.name = "test-app"
    mock_app.location = "eastus"
    mock_app.state = "Running"
    mock_app.default_host_name = "test-app.azurewebsites.net"
    
    mock_client_instance = Mock()
    mock_client_instance.web_apps.list.return_value = [mock_app]
    mock_web_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/app-services", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["appServices"]) > 0

@patch('main.WebSiteManagementClient')
def test_app_service_details(mock_web_client, mock_azure_credentials):
    """Test 9: App Service details endpoint"""
    mock_app = Mock()
    mock_app.name = "test-app"
    mock_app.location = "eastus"
    mock_app.state = "Running"
    mock_app.default_host_name = "test-app.azurewebsites.net"
    mock_app.kind = "app,linux"
    
    mock_config = Mock()
    mock_config.linux_fx_version = "PYTHON|3.12"
    
    mock_client_instance = Mock()
    mock_client_instance.web_apps.get.return_value = mock_app
    mock_client_instance.web_apps.get_configuration.return_value = mock_config
    mock_web_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/app-services/test-rg/test-app", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-app"

@patch('main.StorageManagementClient')
def test_storage_accounts(mock_storage_client, mock_azure_credentials):
    """Test 10: Storage accounts list endpoint"""
    mock_account = Mock()
    mock_account.name = "teststorage"
    mock_account.location = "eastus"
    mock_account.sku.name = "Standard_LRS"
    mock_account.kind = "StorageV2"
    
    mock_client_instance = Mock()
    mock_client_instance.storage_accounts.list.return_value = [mock_account]
    mock_storage_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/storage-accounts", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["storageAccounts"]) > 0

@patch('main.StorageManagementClient')
def test_storage_account_details(mock_storage_client, mock_azure_credentials):
    """Test 11: Storage account details endpoint"""
    mock_account = Mock()
    mock_account.name = "teststorage"
    mock_account.location = "eastus"
    mock_account.sku.name = "Standard_LRS"
    mock_account.kind = "StorageV2"
    mock_account.primary_endpoints.blob = "https://teststorage.blob.core.windows.net/"
    
    mock_client_instance = Mock()
    mock_client_instance.storage_accounts.get_properties.return_value = mock_account
    mock_storage_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/storage-accounts/test-rg/teststorage", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teststorage"

@patch('main.ContainerServiceClient')
def test_aks_node_pools(mock_container_client, mock_azure_credentials):
    """Test 12: AKS node pools endpoint"""
    mock_pool = Mock()
    mock_pool.name = "nodepool1"
    mock_pool.count = 3
    mock_pool.vm_size = "Standard_DS2_v2"
    mock_pool.os_type = "Linux"
    mock_pool.provisioning_state = "Succeeded"
    
    mock_client_instance = Mock()
    mock_client_instance.agent_pools.list.return_value = [mock_pool]
    mock_container_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/aks/node-pools", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["nodePools"]) > 0

@patch('main.client.CoreV1Api')
@patch('main.config.load_kube_config_from_dict')
def test_aks_services(mock_load_config, mock_core_api, mock_azure_credentials):
    """Test 13: AKS services endpoint"""
    mock_service = Mock()
    mock_service.metadata.name = "test-service"
    mock_service.metadata.namespace = "default"
    mock_service.spec.type = "LoadBalancer"
    mock_service.spec.cluster_ip = "10.0.0.1"
    
    mock_service_list = Mock()
    mock_service_list.items = [mock_service]
    
    mock_api_instance = Mock()
    mock_api_instance.list_service_for_all_namespaces.return_value = mock_service_list
    mock_core_api.return_value = mock_api_instance
    
    response = client.get("/api/azure/aks/services", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["services"]) > 0

@patch('main.client.CoreV1Api')
@patch('main.config.load_kube_config_from_dict')
def test_aks_namespaces(mock_load_config, mock_core_api, mock_azure_credentials):
    """Test 14: AKS namespaces endpoint"""
    mock_namespace = Mock()
    mock_namespace.metadata.name = "default"
    mock_namespace.status.phase = "Active"
    
    mock_namespace_list = Mock()
    mock_namespace_list.items = [mock_namespace]
    
    mock_api_instance = Mock()
    mock_api_instance.list_namespace.return_value = mock_namespace_list
    mock_core_api.return_value = mock_api_instance
    
    response = client.get("/api/azure/aks/namespaces", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["namespaces"]) > 0

@patch('main.ResourceManagementClient')
def test_subscription_info(mock_resource_client, mock_azure_credentials):
    """Test 15: Subscription info endpoint"""
    mock_subscription = Mock()
    mock_subscription.subscription_id = "3306e559-a033-43dd-bf98-fc59174d563f"
    mock_subscription.display_name = "Test Subscription"
    mock_subscription.state = "Enabled"
    
    mock_client_instance = Mock()
    mock_client_instance.subscriptions.get.return_value = mock_subscription
    mock_resource_client.return_value = mock_client_instance
    
    response = client.get("/api/azure/subscription", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "subscriptionId" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
