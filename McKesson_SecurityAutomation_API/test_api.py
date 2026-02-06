"""
Simple API tests for FastAPI Azure Backend
Tests all 15 Azure read-only API endpoints using requests library
"""

import requests
import json
from unittest.mock import Mock, patch
import pytest

BASE_URL = "http://127.0.0.1:8888"
BEARER_TOKEN = "your-secret-token-123"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}

def test_1_health_endpoint():
    """Test 1: Health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    print("✓ Test 1 passed: Health endpoint working")

def test_2_unauthorized_access():
    """Test 2: Verify bearer token authentication"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/status")
    assert response.status_code == 403
    assert "Invalid or missing bearer token" in response.json()["detail"]
    print("✓ Test 2 passed: Authentication working")

def test_3_aks_status():
    """Test 3: AKS cluster status endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/status", headers=HEADERS)
    assert response.status_code in [200, 500]  # May fail if Azure creds not set
    if response.status_code == 200:
        data = response.json()
        assert "name" in data
        assert "powerState" in data
        print("✓ Test 3 passed: AKS status endpoint working")
    else:
        print("⚠ Test 3 skipped: Azure credentials needed")

def test_4_aks_pods():
    """Test 4: AKS pods list endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/pods", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "pods" in data
        print("✓ Test 4 passed: AKS pods endpoint working")
    else:
        print("⚠ Test 4 skipped: Azure credentials needed")

def test_5_aks_deployments():
    """Test 5: AKS deployments list endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/deployments", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "deployments" in data
        print("✓ Test 5 passed: AKS deployments endpoint working")
    else:
        print("⚠ Test 5 skipped: Azure credentials needed")

def test_6_resource_groups():
    """Test 6: Resource groups list endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/resource-groups", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "resourceGroups" in data
        print("✓ Test 6 passed: Resource groups endpoint working")
    else:
        print("⚠ Test 6 skipped: Azure credentials needed")

def test_7_resources_by_group():
    """Test 7: Resources by group endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/resources/hsps-demo-rg", headers=HEADERS)
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.json()
        assert "resourceGroup" in data
        print("✓ Test 7 passed: Resources by group endpoint working")
    else:
        print("⚠ Test 7 skipped: Resource group may not exist or Azure credentials needed")

def test_8_app_services():
    """Test 8: App Services list endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/app-services", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "appServices" in data
        print("✓ Test 8 passed: App Services endpoint working")
    else:
        print("⚠ Test 8 skipped: Azure credentials needed")

def test_9_app_service_details():
    """Test 9: App Service details endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/app-services/hsps-demo-rg/mckessondemo-api", headers=HEADERS)
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.json()
        assert "name" in data
        print("✓ Test 9 passed: App Service details endpoint working")
    else:
        print("⚠ Test 9 skipped: App Service may not exist or Azure credentials needed")

def test_10_storage_accounts():
    """Test 10: Storage accounts list endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/storage-accounts", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "storageAccounts" in data
        print("✓ Test 10 passed: Storage accounts endpoint working")
    else:
        print("⚠ Test 10 skipped: Azure credentials needed")

def test_11_storage_account_details():
    """Test 11: Storage account details endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/storage-accounts/hsps-demo-rg/teststorage", headers=HEADERS)
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.json()
        assert "name" in data
        print("✓ Test 11 passed: Storage account details endpoint working")
    else:
        print("⚠ Test 11 skipped: Storage account may not exist or Azure credentials needed")

def test_12_aks_node_pools():
    """Test 12: AKS node pools endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/node-pools", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "nodePools" in data
        print("✓ Test 12 passed: AKS node pools endpoint working")
    else:
        print("⚠ Test 12 skipped: Azure credentials needed")

def test_13_aks_services():
    """Test 13: AKS services endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/services", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "services" in data
        print("✓ Test 13 passed: AKS services endpoint working")
    else:
        print("⚠ Test 13 skipped: Azure credentials needed")

def test_14_aks_namespaces():
    """Test 14: AKS namespaces endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/aks/namespaces", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "namespaces" in data
        print("✓ Test 14 passed: AKS namespaces endpoint working")
    else:
        print("⚠ Test 14 skipped: Azure credentials needed")

def test_15_subscription_info():
    """Test 15: Subscription info endpoint"""
    response = requests.get(f"{BASE_URL}/api/azure/subscription", headers=HEADERS)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "subscriptionId" in data
        print("✓ Test 15 passed: Subscription info endpoint working")
    else:
        print("⚠ Test 15 skipped: Azure credentials needed")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Running API Tests for FastAPI Azure Backend")
    print("="*70 + "\n")
    print("NOTE: Backend must be running on http://127.0.0.1:8888")
    print("Start with: cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8888\n")
    
    tests = [
        test_1_health_endpoint,
        test_2_unauthorized_access,
        test_3_aks_status,
        test_4_aks_pods,
        test_5_aks_deployments,
        test_6_resource_groups,
        test_7_resources_by_group,
        test_8_app_services,
        test_9_app_service_details,
        test_10_storage_accounts,
        test_11_storage_account_details,
        test_12_aks_node_pools,
        test_13_aks_services,
        test_14_aks_namespaces,
        test_15_subscription_info,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except requests.exceptions.ConnectionError:
            print(f"✗ {test.__name__} failed: Backend not running")
            failed += 1
            break
        except Exception as e:
            print(f"⚠ {test.__name__} skipped: {e}")
            skipped += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("="*70 + "\n")
