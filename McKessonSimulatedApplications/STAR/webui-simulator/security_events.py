import random
from datetime import datetime
from typing import Dict

class WebUISecurityEventGenerator:
    def __init__(self, anomaly_frequency: float = 0.1):
        self.anomaly_frequency = anomaly_frequency
        self.event_types = [
            "xss_detection",
            "csrf_failure",
            "bot_detection",
            "file_upload_attempt",
            "geolocation_mismatch",
            "session_hijacking",
            "clickjacking_attempt",
            "form_tampering",
            "suspicious_navigation"
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
            "<iframe src='evil.com'></iframe>",
            "<svg onload=alert(1)>",
            "'-alert(1)-'",
            "\"><script>alert(String.fromCharCode(88,83,83))</script>"
        ]
        
        self.suspicious_files = [
            "malware.exe", "payload.php", "shell.jsp",
            "backdoor.aspx", "exploit.sh", "virus.bat"
        ]
        
        self.locations = [
            {"city": "New York", "country": "US", "lat": 40.7128, "lon": -74.0060},
            {"city": "London", "country": "UK", "lat": 51.5074, "lon": -0.1278},
            {"city": "Moscow", "country": "RU", "lat": 55.7558, "lon": 37.6173},
            {"city": "Beijing", "country": "CN", "lat": 39.9042, "lon": 116.4074},
            {"city": "Lagos", "country": "NG", "lat": 6.5244, "lon": 3.3792}
        ]
    
    def should_generate_event(self) -> bool:
        return random.random() < self.anomaly_frequency
    
    def generate_event(self) -> Dict:
        event_type = random.choice(self.event_types)
        
        if event_type == "xss_detection":
            return self._generate_xss_detection()
        elif event_type == "csrf_failure":
            return self._generate_csrf_failure()
        elif event_type == "bot_detection":
            return self._generate_bot_detection()
        elif event_type == "file_upload_attempt":
            return self._generate_file_upload_attempt()
        elif event_type == "geolocation_mismatch":
            return self._generate_geolocation_mismatch()
        elif event_type == "session_hijacking":
            return self._generate_session_hijacking()
        elif event_type == "clickjacking_attempt":
            return self._generate_clickjacking()
        elif event_type == "form_tampering":
            return self._generate_form_tampering()
        elif event_type == "suspicious_navigation":
            return self._generate_suspicious_navigation()
        
        return {}
    
    def _generate_xss_detection(self) -> Dict:
        return {
            "event_type": "xss_detection",
            "severity": "high",
            "payload": random.choice(self.xss_payloads),
            "input_field": random.choice(["search", "comment", "name", "description", "notes"]),
            "page": random.choice(["/prescriptions", "/medications", "/patients"]),
            "user_id": f"user_{random.randint(100, 999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat(),
            "waf_rule": f"XSS_PROTECTION_{random.randint(1000, 9999)}"
        }
    
    def _generate_csrf_failure(self) -> Dict:
        return {
            "event_type": "csrf_failure",
            "severity": "high",
            "form_action": random.choice(["/submit-prescription", "/update-medication", "/delete-order"]),
            "expected_token": f"token_{random.randint(100000, 999999)}",
            "received_token": random.choice(["missing", "invalid", "expired"]),
            "user_id": f"user_{random.randint(100, 999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "referer": random.choice(["http://evil.com", "http://phishing-site.com", "missing"]),
            "blocked": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_bot_detection(self) -> Dict:
        bot_indicators = [
            "rapid_clicking",
            "no_mouse_movement",
            "automated_form_filling",
            "suspicious_user_agent",
            "headless_browser",
            "missing_javascript"
        ]
        
        return {
            "event_type": "bot_detection",
            "severity": "medium",
            "indicators": random.sample(bot_indicators, k=random.randint(2, 4)),
            "user_agent": random.choice([
                "Mozilla/5.0 (compatible; bot/1.0)",
                "Python-urllib/3.8",
                "curl/7.68.0",
                "Scrapy/2.5.0"
            ]),
            "session_id": f"session_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "pages_visited": random.randint(50, 500),
            "time_on_site_seconds": random.randint(10, 60),
            "actions_per_second": random.uniform(5, 20),
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "captcha_challenge"
        }
    
    def _generate_file_upload_attempt(self) -> Dict:
        return {
            "event_type": "file_upload_attempt",
            "severity": "critical",
            "filename": random.choice(self.suspicious_files),
            "file_type": random.choice(["exe", "php", "jsp", "aspx", "sh", "bat"]),
            "file_size_bytes": random.randint(1000, 10000000),
            "upload_field": "document_upload",
            "user_id": f"user_{random.randint(100, 999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "malware_detected": random.choice([True, False]),
            "status": "blocked",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_geolocation_mismatch(self) -> Dict:
        previous_location = random.choice(self.locations)
        current_location = random.choice([loc for loc in self.locations if loc != previous_location])
        
        return {
            "event_type": "geolocation_mismatch",
            "severity": "medium",
            "user_id": f"user_{random.randint(100, 999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "previous_location": previous_location,
            "current_location": current_location,
            "time_between_logins_minutes": random.randint(1, 30),
            "distance_km": random.randint(1000, 15000),
            "impossible_travel": random.choice([True, False]),
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "additional_verification_required"
        }
    
    def _generate_session_hijacking(self) -> Dict:
        return {
            "event_type": "session_hijacking",
            "severity": "critical",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "original_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "new_ip": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "original_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "new_user_agent": "Mozilla/5.0 (X11; Linux x86_64)",
            "session_token_reuse": True,
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "session_terminated"
        }
    
    def _generate_clickjacking(self) -> Dict:
        return {
            "event_type": "clickjacking_attempt",
            "severity": "high",
            "page": random.choice(["/prescriptions", "/orders", "/admin"]),
            "iframe_detected": True,
            "parent_domain": random.choice(["evil.com", "phishing-site.com", "malicious.net"]),
            "x_frame_options_missing": True,
            "user_id": f"user_{random.randint(100, 999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": True
        }
    
    def _generate_form_tampering(self) -> Dict:
        return {
            "event_type": "form_tampering",
            "severity": "high",
            "form_id": random.choice(["prescription_form", "order_form", "patient_form"]),
            "tampered_fields": random.sample(["price", "quantity", "user_role", "permissions"], k=random.randint(1, 3)),
            "original_values": {"price": "10.00", "quantity": "1"},
            "tampered_values": {"price": "0.01", "quantity": "1000"},
            "user_id": f"user_{random.randint(100, 999)}",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "timestamp": datetime.utcnow().isoformat(),
            "blocked": True
        }
    
    def _generate_suspicious_navigation(self) -> Dict:
        return {
            "event_type": "suspicious_navigation",
            "severity": "medium",
            "pattern": random.choice([
                "rapid_page_enumeration",
                "directory_traversal_attempt",
                "forced_browsing",
                "parameter_manipulation"
            ]),
            "pages_accessed": random.randint(50, 200),
            "time_window_seconds": random.randint(10, 60),
            "suspicious_urls": [
                "/admin/config",
                "/api/internal/users",
                "/../../../etc/passwd",
                "/backup/database.sql"
            ],
            "user_id": f"user_{random.randint(100, 999)}",
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "timestamp": datetime.utcnow().isoformat(),
            "action_taken": "rate_limited"
        }
