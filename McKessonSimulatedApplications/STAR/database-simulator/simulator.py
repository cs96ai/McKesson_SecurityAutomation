import random
import time
from datetime import datetime, timedelta
from typing import Dict, List

class DatabaseSimulator:
    def __init__(self):
        self.active_connections = 0
        self.total_queries = 0
        self.query_history = []
        self.connection_pool_size = 100
        self.tables = [
            "patients", "medications", "prescriptions", "inventory",
            "orders", "users", "audit_logs", "billing", "insurance"
        ]
        self.query_types = ["SELECT", "INSERT", "UPDATE", "DELETE", "JOIN"]
        
    def generate_metrics(self) -> Dict:
        self.active_connections = random.randint(10, 80)
        
        queries_by_type = {}
        for qtype in self.query_types:
            queries_by_type[qtype] = random.randint(5, 50)
        
        query_durations = {}
        for qtype in self.query_types:
            if qtype == "JOIN":
                query_durations[qtype] = random.uniform(0.5, 3.0)
            elif qtype == "SELECT":
                query_durations[qtype] = random.uniform(0.01, 0.5)
            else:
                query_durations[qtype] = random.uniform(0.05, 0.3)
        
        return {
            "active_connections": self.active_connections,
            "pool_utilization": round(self.active_connections / self.connection_pool_size, 2),
            "queries_by_type": queries_by_type,
            "query_durations": query_durations,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_connection_stats(self) -> Dict:
        return {
            "active": self.active_connections,
            "max_pool_size": self.connection_pool_size,
            "utilization_percent": round((self.active_connections / self.connection_pool_size) * 100, 2),
            "idle_connections": self.connection_pool_size - self.active_connections,
            "connection_errors_last_hour": random.randint(0, 5),
            "avg_connection_time_ms": random.uniform(10, 100)
        }
    
    def get_query_stats(self) -> Dict:
        return {
            "total_queries_last_minute": random.randint(100, 500),
            "slow_queries_last_hour": random.randint(0, 10),
            "failed_queries_last_hour": random.randint(0, 3),
            "avg_query_time_ms": random.uniform(50, 200),
            "p95_query_time_ms": random.uniform(200, 500),
            "p99_query_time_ms": random.uniform(500, 1000),
            "cache_hit_ratio": random.uniform(0.7, 0.95),
            "table_scans_last_hour": random.randint(5, 30)
        }
    
    def execute_simulated_query(self, sql: str) -> Dict:
        start_time = time.time()
        
        time.sleep(random.uniform(0.01, 0.2))
        
        duration = time.time() - start_time
        
        rows_affected = random.randint(1, 1000)
        
        query_type = "UNKNOWN"
        for qtype in self.query_types:
            if qtype in sql.upper():
                query_type = qtype
                break
        
        return {
            "status": "success",
            "query_type": query_type,
            "duration": round(duration, 4),
            "rows_affected": rows_affected,
            "execution_plan": f"Sequential Scan on {random.choice(self.tables)}",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def simulate_table_scan(self, table_name: str) -> Dict:
        return {
            "table": table_name,
            "scan_type": "FULL",
            "rows_scanned": random.randint(10000, 1000000),
            "duration_ms": random.uniform(500, 5000),
            "timestamp": datetime.utcnow().isoformat()
        }
