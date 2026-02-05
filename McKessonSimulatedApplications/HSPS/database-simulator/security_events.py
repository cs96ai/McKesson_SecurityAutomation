import random
from datetime import datetime
from typing import Dict

class SecurityEventGenerator:
    def __init__(self, anomaly_frequency: float = 0.1):
        self.anomaly_frequency = anomaly_frequency
        self.event_types = [
            "auth_failure",
            "privilege_escalation",
            "data_exfiltration",
            "sql_injection",
            "connection_spike",
            "failed_login",
            "unusual_query_pattern",
            "brute_force_attack"
        ]
        
        self.usernames = [
            "admin", "dbadmin", "pharmacy_user", "readonly_user",
            "backup_service", "reporting_user", "api_service"
        ]
        
        self.suspicious_usernames = [
            "root", "sa", "postgres", "mysql", "oracle",
            "' OR '1'='1", "admin'--", "test", "guest"
        ]
        
        self.ip_addresses = [
            "10.0.1.100", "10.0.1.101", "10.0.1.102",
            "192.168.1.50", "172.16.0.10"
        ]
        
        self.suspicious_ips = [
            "185.220.101.1", "45.142.212.61", "198.51.100.42",
            "203.0.113.5", "192.0.2.100"
        ]
        
        self.sql_injection_patterns = [
            "' OR '1'='1",
            "'; DROP TABLE users--",
            "UNION SELECT * FROM passwords",
            "1' AND 1=1--",
            "admin'--",
            "' OR 1=1#"
        ]
    
    def should_generate_event(self) -> bool:
        return random.random() < self.anomaly_frequency
    
    def generate_event(self) -> Dict:
        event_type = random.choice(self.event_types)
        
        if event_type == "auth_failure":
            return self._generate_auth_failure()
        elif event_type == "privilege_escalation":
            return self._generate_privilege_escalation()
        elif event_type == "data_exfiltration":
            return self._generate_data_exfiltration()
        elif event_type == "sql_injection":
            return self._generate_sql_injection()
        elif event_type == "connection_spike":
            return self._generate_connection_spike()
        elif event_type == "failed_login":
            return self._generate_failed_login()
        elif event_type == "unusual_query_pattern":
            return self._generate_unusual_query()
        elif event_type == "brute_force_attack":
            return self._generate_brute_force()
        
        return {}
    
    def _generate_auth_failure(self) -> Dict:
        reasons = [
            "invalid_credentials",
            "expired_password",
            "account_locked",
            "invalid_certificate",
            "missing_mfa"
        ]
        
        return {
            "event_type": "auth_failure",
            "severity": "medium",
            "username": random.choice(self.usernames + self.suspicious_usernames),
            "source_ip": random.choice(self.ip_addresses + self.suspicious_ips),
            "reason": random.choice(reasons),
            "timestamp": datetime.utcnow().isoformat(),
            "database": "hsps_pharmacy",
            "attempt_count": random.randint(1, 10)
        }
    
    def _generate_privilege_escalation(self) -> Dict:
        actions = [
            "ALTER USER SET ROLE admin",
            "GRANT ALL PRIVILEGES",
            "CREATE USER WITH SUPERUSER",
            "ALTER SYSTEM SET",
            "COPY TO PROGRAM"
        ]
        
        return {
            "event_type": "privilege_escalation",
            "severity": "high",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses + self.suspicious_ips),
            "attempted_action": random.choice(actions),
            "current_role": "user",
            "target_role": "admin",
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": random.choice([True, False])
        }
    
    def _generate_data_exfiltration(self) -> Dict:
        return {
            "event_type": "data_exfiltration",
            "severity": "critical",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "destination_ip": random.choice(self.suspicious_ips),
            "bytes_transferred": random.randint(10000000, 1000000000),
            "records_accessed": random.randint(1000, 100000),
            "tables": random.sample(["patients", "medications", "prescriptions", "billing"], k=random.randint(1, 3)),
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": random.randint(60, 3600)
        }
    
    def _generate_sql_injection(self) -> Dict:
        return {
            "event_type": "sql_injection",
            "severity": "high",
            "source_ip": random.choice(self.suspicious_ips),
            "injection_pattern": random.choice(self.sql_injection_patterns),
            "target_table": random.choice(["users", "patients", "medications"]),
            "query_fragment": f"SELECT * FROM users WHERE username='{random.choice(self.sql_injection_patterns)}'",
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat(),
            "waf_rule_triggered": f"SQL_INJECTION_{random.randint(1000, 9999)}"
        }
    
    def _generate_connection_spike(self) -> Dict:
        return {
            "event_type": "connection_spike",
            "severity": "medium",
            "baseline_connections": random.randint(20, 50),
            "current_connections": random.randint(200, 500),
            "spike_percentage": random.randint(300, 1000),
            "source_ips": random.sample(self.ip_addresses + self.suspicious_ips, k=random.randint(3, 7)),
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": random.randint(30, 300),
            "potential_ddos": random.choice([True, False])
        }
    
    def _generate_failed_login(self) -> Dict:
        return {
            "event_type": "failed_login",
            "severity": "low",
            "username": random.choice(self.suspicious_usernames),
            "source_ip": random.choice(self.suspicious_ips),
            "failure_reason": random.choice(["invalid_password", "user_not_found", "account_disabled"]),
            "attempt_number": random.randint(1, 20),
            "timestamp": datetime.utcnow().isoformat(),
            "user_agent": "psql/14.5"
        }
    
    def _generate_unusual_query(self) -> Dict:
        patterns = [
            "SELECT * FROM information_schema.tables",
            "SELECT * FROM pg_shadow",
            "COPY (SELECT * FROM patients) TO '/tmp/data.csv'",
            "SELECT COUNT(*) FROM patients WHERE 1=1",
            "DELETE FROM audit_logs WHERE timestamp < NOW()"
        ]
        
        return {
            "event_type": "unusual_query_pattern",
            "severity": "medium",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "query_pattern": random.choice(patterns),
            "execution_time_ms": random.uniform(5000, 30000),
            "rows_affected": random.randint(10000, 1000000),
            "timestamp": datetime.utcnow().isoformat(),
            "flagged_reason": random.choice([
                "full_table_scan",
                "excessive_rows",
                "system_table_access",
                "data_export_attempt"
            ])
        }
    
    def _generate_brute_force(self) -> Dict:
        return {
            "event_type": "brute_force_attack",
            "severity": "high",
            "target_username": random.choice(self.usernames),
            "source_ip": random.choice(self.suspicious_ips),
            "attempt_count": random.randint(50, 500),
            "time_window_seconds": random.randint(60, 600),
            "success_count": 0,
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": True,
            "rate_limit_triggered": True
        }
