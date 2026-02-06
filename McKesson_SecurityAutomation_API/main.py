"""
FastAPI Backend for Azure Read-Only Operations

This FastAPI server provides secure backend endpoints for Azure API calls.
Uses the read-only service principal to ensure no write operations are possible.
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.storage import StorageManagementClient
from kubernetes import client, config
from typing import Optional, List
from pydantic import BaseModel
import os
import json
import yaml
import base64
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv('.env.production')

app = FastAPI(title="Azure API Backend", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Configuration
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "3306e559-a033-43dd-bf98-fc59174d563f")
RESOURCE_GROUP = "hsps-demo-rg"
AKS_CLUSTER_NAME = "hsps-aks-cluster"
BEARER_TOKEN = os.getenv("VITE_BEARER_TOKEN", "your-secret-token-123")

# Initialize Azure credentials
credential = ClientSecretCredential(
    tenant_id=os.getenv("VITE_AZURE_TENANT_ID"),
    client_id=os.getenv("VITE_AZURE_CLIENT_ID"),
    client_secret=os.getenv("VITE_AZURE_CLIENT_SECRET")
)

# Initialize Azure clients
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
aks_client = ContainerServiceClient(credential, SUBSCRIPTION_ID)
web_client = WebSiteManagementClient(credential, SUBSCRIPTION_ID)
storage_client = StorageManagementClient(credential, SUBSCRIPTION_ID)

# Bearer token authentication
async def verify_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer" or token != BEARER_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    return token

# Helper function to calculate pod age
def calculate_age(timestamp_str: str) -> str:
    created = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    now = datetime.now(created.tzinfo)
    diff = now - created
    
    minutes = diff.total_seconds() / 60
    if minutes < 60:
        return f"{int(minutes)}m"
    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)}h"
    days = hours / 24
    return f"{int(days)}d"

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# 1. Get AKS Cluster Status
@app.get("/api/azure/aks/status", dependencies=[Depends(verify_token)])
async def get_aks_status():
    try:
        cluster = aks_client.managed_clusters.get(RESOURCE_GROUP, AKS_CLUSTER_NAME)
        return {
            "name": cluster.name,
            "location": cluster.location,
            "powerState": cluster.power_state.code if cluster.power_state else "Unknown",
            "provisioningState": cluster.provisioning_state,
            "kubernetesVersion": cluster.kubernetes_version,
            "nodeResourceGroup": cluster.node_resource_group,
            "fqdn": cluster.fqdn,
            "agentPoolProfiles": [
                {
                    "name": pool.name,
                    "count": pool.count,
                    "vmSize": pool.vm_size,
                    "osType": pool.os_type
                }
                for pool in (cluster.agent_pool_profiles or [])
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2 & 3. List Pods in Namespace
@app.get("/api/azure/pods/{namespace}", dependencies=[Depends(verify_token)])
async def list_pods(namespace: str):
    try:
        # Get AKS credentials
        credentials = aks_client.managed_clusters.list_cluster_user_credentials(
            RESOURCE_GROUP, AKS_CLUSTER_NAME
        )
        
        # Load kubeconfig
        kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
        
        # List pods
        v1 = client.CoreV1Api()
        pods_list = v1.list_namespaced_pod(namespace)
        
        pods = []
        for pod in pods_list.items:
            ready = all(c.ready for c in (pod.status.container_statuses or []))
            restarts = sum(c.restart_count for c in (pod.status.container_statuses or []))
            
            pods.append({
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "ready": ready,
                "restarts": restarts,
                "age": calculate_age(pod.metadata.creation_timestamp.isoformat()),
                "ip": pod.status.pod_ip
            })
        
        return {"namespace": namespace, "pods": pods, "count": len(pods)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Get Pod Details
@app.get("/api/azure/pods/{namespace}/{pod_name}", dependencies=[Depends(verify_token)])
async def get_pod_details(namespace: str, pod_name: str):
    try:
        credentials = aks_client.managed_clusters.list_cluster_user_credentials(
            RESOURCE_GROUP, AKS_CLUSTER_NAME
        )
        
        kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
        
        v1 = client.CoreV1Api()
        pod = v1.read_namespaced_pod(pod_name, namespace)
        
        return {
            "name": pod.metadata.name,
            "namespace": pod.metadata.namespace,
            "status": pod.status.phase,
            "ip": pod.status.pod_ip,
            "node": pod.spec.node_name,
            "creationTimestamp": pod.metadata.creation_timestamp.isoformat(),
            "labels": pod.metadata.labels,
            "containers": [
                {
                    "name": c.name,
                    "image": c.image,
                    "ports": [{"containerPort": p.container_port, "protocol": p.protocol} for p in (c.ports or [])]
                }
                for c in pod.spec.containers
            ],
            "conditions": [
                {"type": c.type, "status": c.status}
                for c in (pod.status.conditions or [])
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Get Resource Group Information
@app.get("/api/azure/resourcegroup/{rg_name}", dependencies=[Depends(verify_token)])
async def get_resource_group(rg_name: str):
    try:
        rg = resource_client.resource_groups.get(rg_name)
        return {
            "name": rg.name,
            "location": rg.location,
            "provisioningState": rg.properties.provisioning_state,
            "tags": rg.tags
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. List All Resources
@app.get("/api/azure/resources/list", dependencies=[Depends(verify_token)])
async def list_resources():
    try:
        resources = []
        for resource in resource_client.resources.list_by_resource_group(RESOURCE_GROUP):
            resources.append({
                "name": resource.name,
                "type": resource.type,
                "location": resource.location,
                "id": resource.id
            })
        
        return {"resourceGroup": RESOURCE_GROUP, "resources": resources, "count": len(resources)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Get App Service Status
@app.get("/api/azure/appservice/{app_name}/status", dependencies=[Depends(verify_token)])
async def get_app_service_status(app_name: str):
    try:
        app = web_client.web_apps.get(RESOURCE_GROUP, app_name)
        return {
            "name": app.name,
            "state": app.state,
            "hostNames": app.host_names,
            "location": app.location,
            "kind": app.kind,
            "httpsOnly": app.https_only,
            "defaultHostName": app.default_host_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. Get Function App Status
@app.get("/api/azure/functionapp/{function_name}/status", dependencies=[Depends(verify_token)])
async def get_function_app_status(function_name: str):
    try:
        function_app = web_client.web_apps.get(RESOURCE_GROUP, function_name)
        return {
            "name": function_app.name,
            "state": function_app.state,
            "hostNames": function_app.host_names,
            "location": function_app.location,
            "kind": function_app.kind,
            "defaultHostName": function_app.default_host_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Get Storage Account Information
@app.get("/api/azure/storage/{account_name}/info", dependencies=[Depends(verify_token)])
async def get_storage_account_info(account_name: str):
    try:
        account = storage_client.storage_accounts.get_properties(RESOURCE_GROUP, account_name)
        return {
            "name": account.name,
            "location": account.location,
            "sku": {"name": account.sku.name, "tier": account.sku.tier.value} if account.sku else None,
            "kind": account.kind.value if account.kind else None,
            "provisioningState": account.provisioning_state.value if account.provisioning_state else None,
            "primaryEndpoints": {
                "blob": account.primary_endpoints.blob if account.primary_endpoints else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. Get AKS Node Pools
@app.get("/api/azure/aks/nodepools", dependencies=[Depends(verify_token)])
async def get_node_pools():
    try:
        node_pools = []
        for pool in aks_client.agent_pools.list(RESOURCE_GROUP, AKS_CLUSTER_NAME):
            node_pools.append({
                "name": pool.name,
                "count": pool.count,
                "vmSize": pool.vm_size,
                "osType": pool.os_type,
                "provisioningState": pool.provisioning_state,
                "powerState": pool.power_state.code if pool.power_state else None
            })
        
        return {"nodePools": node_pools, "count": len(node_pools)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 11. Get Deployment Status
@app.get("/api/azure/deployments/{namespace}", dependencies=[Depends(verify_token)])
async def get_deployments(namespace: str):
    try:
        credentials = aks_client.managed_clusters.list_cluster_user_credentials(
            RESOURCE_GROUP, AKS_CLUSTER_NAME
        )
        
        kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
        
        apps_v1 = client.AppsV1Api()
        deployments_list = apps_v1.list_namespaced_deployment(namespace)
        
        deployments = []
        for dep in deployments_list.items:
            deployments.append({
                "name": dep.metadata.name,
                "replicas": dep.spec.replicas,
                "availableReplicas": dep.status.available_replicas or 0,
                "readyReplicas": dep.status.ready_replicas or 0,
                "updatedReplicas": dep.status.updated_replicas or 0
            })
        
        return {"namespace": namespace, "deployments": deployments, "count": len(deployments)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 12. Get Service Status
@app.get("/api/azure/services/{namespace}", dependencies=[Depends(verify_token)])
async def get_services(namespace: str):
    try:
        credentials = aks_client.managed_clusters.list_cluster_user_credentials(
            RESOURCE_GROUP, AKS_CLUSTER_NAME
        )
        
        kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
        
        v1 = client.CoreV1Api()
        services_list = v1.list_namespaced_service(namespace)
        
        services = []
        for svc in services_list.items:
            services.append({
                "name": svc.metadata.name,
                "type": svc.spec.type,
                "clusterIP": svc.spec.cluster_ip,
                "ports": [
                    {"port": p.port, "targetPort": str(p.target_port), "protocol": p.protocol}
                    for p in (svc.spec.ports or [])
                ]
            })
        
        return {"namespace": namespace, "services": services, "count": len(services)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 13. Get Pod Logs
@app.get("/api/azure/pods/{namespace}/{pod_name}/logs", dependencies=[Depends(verify_token)])
async def get_pod_logs(namespace: str, pod_name: str):
    try:
        credentials = aks_client.managed_clusters.list_cluster_user_credentials(
            RESOURCE_GROUP, AKS_CLUSTER_NAME
        )
        
        kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
        config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
        
        v1 = client.CoreV1Api()
        logs = v1.read_namespaced_pod_log(
            pod_name,
            namespace,
            tail_lines=50
        )
        
        return {
            "podName": pod_name,
            "namespace": namespace,
            "logs": logs.split('\n')[-50:]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 14. Get Subscription Information (Non-Sensitive)
@app.get("/api/azure/subscription/info", dependencies=[Depends(verify_token)])
async def get_subscription_info():
    try:
        subscription = resource_client.subscriptions.get(SUBSCRIPTION_ID)
        return {
            "displayName": subscription.display_name,
            "state": subscription.state.value if subscription.state else None,
            "subscriptionId": f"{SUBSCRIPTION_ID[:5]}***********************************"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 15. Get Cost Analysis (Simulated)
@app.get("/api/azure/costs/summary", dependencies=[Depends(verify_token)])
async def get_cost_analysis():
    return {
        "period": "Last 30 days",
        "totalCost": "$127.45",
        "breakdown": [
            {"service": "Azure Kubernetes Service", "cost": "$45.20"},
            {"service": "App Service", "cost": "$32.10"},
            {"service": "Function App", "cost": "$15.80"},
            {"service": "Storage Account", "cost": "$12.35"},
            {"service": "Other", "cost": "$22.00"}
        ],
        "note": "Cost data is simulated. Enable Cost Management API for real data."
    }

# ============================================================
# OpenAI Agent with Function Calling
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

AGENT_SYSTEM_PROMPT = """You are a read-only operations assistant for the McKesson Security Automation Platform. You support operations engineers who manage Azure infrastructure and Kubernetes workloads.

You have access to live Azure and Kubernetes tools. Use them to retrieve real data when answering questions — never speculate when you can look it up.

PERSONALITY:
- Be direct and professional — no fluff, but not cold either.
- Be thoughtful: consider what the user is really trying to accomplish. If they ask about pod status, they may be troubleshooting an outage — proactively mention anything that looks unhealthy.
- Be patient: if a question is ambiguous, ask a brief clarifying question before making assumptions.
- Be forthcoming: if you notice something unusual in the data (high restart counts, pods not ready, services down), flag it even if the user didn't ask.
- Think like an operations engineer: consider dependencies, upstream/downstream impacts, and common failure patterns.

RULES:
1. READ-ONLY: You can only retrieve and report information. You cannot modify, delete, or scale any resources.
2. Use the appropriate tools to fetch live data. If a question spans multiple areas, call multiple tools to give a complete picture.
3. Format responses clearly. Use bullet points or tables for lists of pods, resources, etc.
4. If a tool call fails, explain what happened and suggest what the user can check.
5. NEVER provide Azure credentials, API keys, secrets, tokens, subscription IDs, or connection strings.
6. If asked to perform a write operation, politely explain that you're read-only and suggest how they could do it themselves.

ENVIRONMENT:
- Kubernetes namespaces: hsps, star
- Resource group: hsps-demo-rg
- AKS cluster: hsps-aks-cluster
"""

# Define all tools that OpenAI can call
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_aks_cluster_status",
            "description": "Get the current status and health of the AKS Kubernetes cluster including power state, version, and node pools",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_pods",
            "description": "List all pods running in a Kubernetes namespace. Use 'hsps' for HSPS pods or 'star' for STAR pods.",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace (hsps or star)", "enum": ["hsps", "star"]}
                },
                "required": ["namespace"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pod_details",
            "description": "Get detailed information about a specific pod by name and namespace",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace"},
                    "pod_name": {"type": "string", "description": "Name of the pod"}
                },
                "required": ["namespace", "pod_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_resource_group_info",
            "description": "Get information about an Azure resource group",
            "parameters": {
                "type": "object",
                "properties": {
                    "rg_name": {"type": "string", "description": "Resource group name", "default": "hsps-demo-rg"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_resources",
            "description": "List all Azure resources in the resource group",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_app_service_status",
            "description": "Get the status of an Azure App Service web app",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "App Service name"}
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_function_app_status",
            "description": "Get the status of an Azure Function App",
            "parameters": {
                "type": "object",
                "properties": {
                    "function_name": {"type": "string", "description": "Function App name"}
                },
                "required": ["function_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_storage_account_info",
            "description": "Get information about an Azure Storage Account",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_name": {"type": "string", "description": "Storage account name"}
                },
                "required": ["account_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_aks_node_pools",
            "description": "Get AKS node pool configuration and status",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_deployments",
            "description": "Get Kubernetes deployment status in a namespace",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace (hsps or star)", "enum": ["hsps", "star"]}
                },
                "required": ["namespace"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_services",
            "description": "Get Kubernetes service status in a namespace",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace (hsps or star)", "enum": ["hsps", "star"]}
                },
                "required": ["namespace"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pod_logs",
            "description": "Get the last 50 lines of logs from a specific pod",
            "parameters": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "Kubernetes namespace"},
                    "pod_name": {"type": "string", "description": "Name of the pod"}
                },
                "required": ["namespace", "pod_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_subscription_info",
            "description": "Get Azure subscription information (non-sensitive)",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cost_analysis",
            "description": "Get cost analysis summary for the last 30 days",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

# Map tool names to actual handler functions
async def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Execute a tool call and return the result"""
    try:
        if tool_name == "get_aks_cluster_status":
            cluster = aks_client.managed_clusters.get(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            return {
                "name": cluster.name, "location": cluster.location,
                "powerState": cluster.power_state.code if cluster.power_state else "Unknown",
                "provisioningState": cluster.provisioning_state,
                "kubernetesVersion": cluster.kubernetes_version,
                "fqdn": cluster.fqdn,
                "agentPoolProfiles": [
                    {"name": p.name, "count": p.count, "vmSize": p.vm_size, "osType": p.os_type}
                    for p in (cluster.agent_pool_profiles or [])
                ]
            }

        elif tool_name == "list_pods":
            ns = arguments.get("namespace", "hsps")
            credentials = aks_client.managed_clusters.list_cluster_user_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
            config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
            v1 = client.CoreV1Api()
            pods_list = v1.list_namespaced_pod(ns)
            pods = []
            for pod in pods_list.items:
                ready = all(c.ready for c in (pod.status.container_statuses or []))
                restarts = sum(c.restart_count for c in (pod.status.container_statuses or []))
                pods.append({
                    "name": pod.metadata.name, "status": pod.status.phase,
                    "ready": ready, "restarts": restarts, "ip": pod.status.pod_ip
                })
            return {"namespace": ns, "pods": pods, "count": len(pods)}

        elif tool_name == "get_pod_details":
            ns = arguments.get("namespace", "hsps")
            pod_name = arguments.get("pod_name")
            credentials = aks_client.managed_clusters.list_cluster_user_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
            config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
            v1 = client.CoreV1Api()
            pod = v1.read_namespaced_pod(pod_name, ns)
            return {
                "name": pod.metadata.name, "namespace": pod.metadata.namespace,
                "status": pod.status.phase, "ip": pod.status.pod_ip, "node": pod.spec.node_name,
                "containers": [{"name": c.name, "image": c.image} for c in pod.spec.containers]
            }

        elif tool_name == "get_resource_group_info":
            rg_name = arguments.get("rg_name", RESOURCE_GROUP)
            rg = resource_client.resource_groups.get(rg_name)
            return {"name": rg.name, "location": rg.location, "provisioningState": rg.properties.provisioning_state, "tags": rg.tags}

        elif tool_name == "list_all_resources":
            resources = []
            for r in resource_client.resources.list_by_resource_group(RESOURCE_GROUP):
                resources.append({"name": r.name, "type": r.type, "location": r.location})
            return {"resourceGroup": RESOURCE_GROUP, "resources": resources, "count": len(resources)}

        elif tool_name == "get_app_service_status":
            app_name = arguments.get("app_name", "mckessondemo-csutherland")
            a = web_client.web_apps.get(RESOURCE_GROUP, app_name)
            return {"name": a.name, "state": a.state, "hostNames": a.host_names, "defaultHostName": a.default_host_name}

        elif tool_name == "get_function_app_status":
            fn = arguments.get("function_name", "hsps-pod-shutdown")
            fa = web_client.web_apps.get(RESOURCE_GROUP, fn)
            return {"name": fa.name, "state": fa.state, "hostNames": fa.host_names, "defaultHostName": fa.default_host_name}

        elif tool_name == "get_storage_account_info":
            acct = arguments.get("account_name", "hspspodshutdown")
            account = storage_client.storage_accounts.get_properties(RESOURCE_GROUP, acct)
            return {"name": account.name, "location": account.location, "kind": str(account.kind) if account.kind else None}

        elif tool_name == "get_aks_node_pools":
            pools = []
            for pool in aks_client.agent_pools.list(RESOURCE_GROUP, AKS_CLUSTER_NAME):
                pools.append({"name": pool.name, "count": pool.count, "vmSize": pool.vm_size, "provisioningState": pool.provisioning_state})
            return {"nodePools": pools, "count": len(pools)}

        elif tool_name == "get_deployments":
            ns = arguments.get("namespace", "hsps")
            credentials = aks_client.managed_clusters.list_cluster_user_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
            config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
            apps_v1 = client.AppsV1Api()
            deps = apps_v1.list_namespaced_deployment(ns)
            return {"namespace": ns, "deployments": [{"name": d.metadata.name, "replicas": d.spec.replicas, "available": d.status.available_replicas or 0} for d in deps.items], "count": len(deps.items)}

        elif tool_name == "get_services":
            ns = arguments.get("namespace", "hsps")
            credentials = aks_client.managed_clusters.list_cluster_user_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
            config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
            v1 = client.CoreV1Api()
            svcs = v1.list_namespaced_service(ns)
            return {"namespace": ns, "services": [{"name": s.metadata.name, "type": s.spec.type, "clusterIP": s.spec.cluster_ip} for s in svcs.items], "count": len(svcs.items)}

        elif tool_name == "get_pod_logs":
            ns = arguments.get("namespace", "hsps")
            pod_name = arguments.get("pod_name")
            credentials = aks_client.managed_clusters.list_cluster_user_credentials(RESOURCE_GROUP, AKS_CLUSTER_NAME)
            kubeconfig_data = credentials.kubeconfigs[0].value.decode('utf-8')
            config.load_kube_config_from_dict(yaml.safe_load(kubeconfig_data))
            v1 = client.CoreV1Api()
            logs = v1.read_namespaced_pod_log(pod_name, ns, tail_lines=50)
            return {"podName": pod_name, "namespace": ns, "logs": logs.split('\n')[-50:]}

        elif tool_name == "get_subscription_info":
            sub = resource_client.subscriptions.get(SUBSCRIPTION_ID)
            return {"displayName": sub.display_name, "state": sub.state.value if sub.state else None}

        elif tool_name == "get_cost_analysis":
            return {
                "period": "Last 30 days", "totalCost": "$127.45",
                "breakdown": [
                    {"service": "Azure Kubernetes Service", "cost": "$45.20"},
                    {"service": "App Service", "cost": "$32.10"},
                    {"service": "Function App", "cost": "$15.80"},
                    {"service": "Storage Account", "cost": "$12.35"},
                    {"service": "Other", "cost": "$22.00"}
                ],
                "note": "Cost data is simulated."
            }

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    except Exception as e:
        return {"error": str(e)}


# Pydantic models for agent chat
class ChatMessage(BaseModel):
    role: str
    content: str

class AgentChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class AgentChatResponse(BaseModel):
    response: str
    tool_calls_made: List[str] = []


@app.post("/api/agent/chat", dependencies=[Depends(verify_token)])
async def agent_chat(request: AgentChatRequest):
    """
    AI Agent endpoint using OpenAI function calling.
    
    Flow:
    1. User sends question
    2. OpenAI decides which tool(s) to call
    3. Backend executes tool calls against Azure/K8s
    4. Results sent back to OpenAI for formatting
    5. Formatted response returned to user
    """
    if not openai_client:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured. Set OPENAI_API_KEY in environment.")

    # Build conversation messages
    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    
    # Add conversation history (last 20 messages)
    for msg in request.history[-20:]:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add current user message
    messages.append({"role": "user", "content": request.message})

    tool_calls_made = []

    try:
        # Step 1: Send to OpenAI with tools
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=AGENT_TOOLS,
            tool_choice="auto",
            max_tokens=1000,
            temperature=0.3
        )

        assistant_message = response.choices[0].message

        # Step 2: If OpenAI wants to call tools, execute them
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        while assistant_message.tool_calls and iteration < max_iterations:
            iteration += 1
            
            # Add assistant message with tool calls to conversation
            messages.append(assistant_message)

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                
                tool_calls_made.append(fn_name)
                
                # Execute the tool
                result = await execute_tool(fn_name, fn_args)
                
                # Add tool result to conversation
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Step 3: Send results back to OpenAI for formatting
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=AGENT_TOOLS,
                tool_choice="auto",
                max_tokens=1000,
                temperature=0.3
            )

            assistant_message = response.choices[0].message

        # Return the final formatted response
        return AgentChatResponse(
            response=assistant_message.content or "I wasn't able to generate a response. Please try again.",
            tool_calls_made=tool_calls_made
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
