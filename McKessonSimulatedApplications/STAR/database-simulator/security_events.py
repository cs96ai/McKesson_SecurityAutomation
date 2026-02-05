import random
from datetime import datetime
from typing import Dict

class SecurityEventGenerator:
    def __init__(self, anomaly_frequency: float = 0.1):
        self.anomaly_frequency = anomaly_frequency
        self.event_types = [
            "auth_failure",
            "privilege_escalation",
            "prescription_data_access",
            "patient_phi_exfiltration",
            "controlled_substance_query",
            "sql_injection",
            "dea_number_access",
            "failed_login",
            "unusual_query_pattern",
            "inventory_tampering",
            "after_hours_access",
            "brute_force_attack"
        ]
        
        self.usernames = [
            "pharmacist_jdoe", "tech_msmith", "pharmacy_manager", "inventory_clerk",
            "billing_service", "reporting_user", "pos_terminal_1", "pos_terminal_2",
            "rx_processing", "insurance_verify"
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
            "'; DROP TABLE prescriptions--",
            "UNION SELECT * FROM patient_records",
            "1' AND 1=1--",
            "'; SELECT * FROM controlled_substances--",
            "' OR 1=1#",
            "UNION SELECT dea_number, npi FROM pharmacists"
        ]
    
    def should_generate_event(self) -> bool:
        return random.random() < self.anomaly_frequency
    
    def generate_event(self) -> Dict:
        event_type = random.choice(self.event_types)
        
        if event_type == "auth_failure":
            return self._generate_auth_failure()
        elif event_type == "privilege_escalation":
            return self._generate_privilege_escalation()
        elif event_type == "prescription_data_access":
            return self._generate_prescription_access()
        elif event_type == "patient_phi_exfiltration":
            return self._generate_phi_exfiltration()
        elif event_type == "controlled_substance_query":
            return self._generate_controlled_substance_query()
        elif event_type == "sql_injection":
            return self._generate_sql_injection()
        elif event_type == "dea_number_access":
            return self._generate_dea_access()
        elif event_type == "failed_login":
            return self._generate_failed_login()
        elif event_type == "unusual_query_pattern":
            return self._generate_unusual_query()
        elif event_type == "inventory_tampering":
            return self._generate_inventory_tampering()
        elif event_type == "after_hours_access":
            return self._generate_after_hours_access()
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
            "database": "star_pharmacy",
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
            "tables": random.sample(["patients", "prescriptions", "controlled_substances", "dea_records", "insurance_claims"], k=random.randint(1, 3)),
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
            "source_ip": random.choice(self.suspicious_ips),
            "target_username": random.choice(self.usernames),
            "attempts": random.randint(50, 500),
            "time_window_seconds": random.randint(60, 300),
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": random.choice([True, False]),
            "attack_pattern": random.choice([
                "dictionary_attack",
                "credential_stuffing",
                "password_spraying"
            ])
        }
    
    def _generate_prescription_access(self) -> Dict:
        medications = ["Oxycodone", "Hydrocodone", "Adderall", "Xanax", "Morphine", "Fentanyl"]
        return {
            "event_type": "prescription_data_access",
            "severity": "high",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "prescription_id": f"RX{random.randint(100000, 999999)}",
            "patient_id": f"PT{random.randint(10000, 99999)}",
            "medication": random.choice(medications),
            "access_reason": random.choice(["lookup", "modification", "deletion", "export"]),
            "timestamp": datetime.utcnow().isoformat(),
            "authorized": random.choice([True, False]),
            "controlled_substance": True
        }
    
    def _generate_phi_exfiltration(self) -> Dict:
        return {
            "event_type": "patient_phi_exfiltration",
            "severity": "critical",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "destination_ip": random.choice(self.suspicious_ips),
            "patient_records_accessed": random.randint(100, 10000),
            "data_types": random.sample(["ssn", "dob", "address", "insurance", "medical_history", "prescriptions"], k=random.randint(2, 4)),
            "bytes_transferred": random.randint(1000000, 100000000),
            "timestamp": datetime.utcnow().isoformat(),
            "hipaa_violation": True,
            "blocked": random.choice([True, False])
        }
    
    def _generate_controlled_substance_query(self) -> Dict:
        schedules = ["Schedule II", "Schedule III", "Schedule IV"]
        return {
            "event_type": "controlled_substance_query",
            "severity": "medium",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "drug_schedule": random.choice(schedules),
            "query_type": random.choice(["inventory_check", "dispense_history", "bulk_export", "audit_report"]),
            "records_returned": random.randint(10, 5000),
            "timestamp": datetime.utcnow().isoformat(),
            "requires_dea_authorization": True,
            "flagged": random.random() < 0.3
        }
    
    def _generate_dea_access(self) -> Dict:
        return {
            "event_type": "dea_number_access",
            "severity": "high",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "dea_number": f"A{random.choice(['B', 'F', 'M'])}{random.randint(1000000, 9999999)}",
            "pharmacist_npi": f"{random.randint(1000000000, 9999999999)}",
            "access_type": random.choice(["view", "modify", "export", "verify"]),
            "timestamp": datetime.utcnow().isoformat(),
            "authorized": random.choice([True, False]),
            "audit_required": True
        }
    
    def _generate_inventory_tampering(self) -> Dict:
        medications = ["Oxycodone 30mg", "Hydrocodone 10mg", "Adderall XR 20mg", "Alprazolam 2mg"]
        return {
            "event_type": "inventory_tampering",
            "severity": "critical",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "medication": random.choice(medications),
            "action": random.choice(["quantity_adjustment", "deletion", "manual_override", "backdated_entry"]),
            "quantity_change": random.randint(-500, -10),
            "ndc_code": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}-{random.randint(10, 99)}",
            "timestamp": datetime.utcnow().isoformat(),
            "requires_investigation": True,
            "discrepancy_detected": True
        }
    
    def _generate_after_hours_access(self) -> Dict:
        return {
            "event_type": "after_hours_access",
            "severity": "medium",
            "username": random.choice(self.usernames),
            "source_ip": random.choice(self.ip_addresses),
            "access_time": "02:47 AM",
            "day_of_week": random.choice(["Saturday", "Sunday", "Monday"]),
            "tables_accessed": random.sample(["prescriptions", "controlled_substances", "patient_records", "dea_logs"], k=random.randint(1, 3)),
            "queries_executed": random.randint(5, 50),
            "timestamp": datetime.utcnow().isoformat(),
            "business_justification": random.choice([None, "emergency_fill", "inventory_audit", "system_maintenance"]),
            "flagged_for_review": True
        }
