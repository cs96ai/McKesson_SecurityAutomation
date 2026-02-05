import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List

class WebUISimulator:
    def __init__(self):
        self.active_sessions = 0
        self.total_page_views = 0
        self.pages = [
            "/", "/prescriptions", "/medications", "/inventory",
            "/orders", "/patients", "/reports", "/admin"
        ]
        self.event_types = [
            "click", "scroll", "form_submit", "search",
            "navigation", "download", "print"
        ]
        
    def generate_metrics(self) -> Dict:
        self.active_sessions = random.randint(20, 150)
        
        page_views = {}
        for page in self.pages:
            page_views[page] = random.randint(5, 50)
        
        page_load_times = {}
        for page in self.pages:
            page_load_times[page] = random.uniform(0.5, 3.0)
        
        clickstream_events = {}
        for event_type in self.event_types:
            clickstream_events[event_type] = random.randint(10, 100)
        
        return {
            "active_sessions": self.active_sessions,
            "page_views": page_views,
            "page_load_times": page_load_times,
            "clickstream_events": clickstream_events,
            "bounce_rate": round(random.uniform(0.2, 0.5), 2),
            "avg_session_duration_seconds": random.randint(120, 600),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_session_stats(self) -> Dict:
        return {
            "active_sessions": self.active_sessions,
            "total_sessions_today": random.randint(500, 2000),
            "avg_session_duration_minutes": random.uniform(5, 30),
            "new_users_percent": random.uniform(10, 40),
            "returning_users_percent": random.uniform(60, 90),
            "mobile_users_percent": random.uniform(20, 50),
            "desktop_users_percent": random.uniform(50, 80),
            "bounce_rate": random.uniform(0.2, 0.5),
            "pages_per_session": random.uniform(3, 10),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_clickstream_data(self) -> List[Dict]:
        events = []
        for _ in range(random.randint(10, 30)):
            events.append({
                "event_id": str(uuid.uuid4()),
                "session_id": f"session_{random.randint(1000, 9999)}",
                "user_id": f"user_{random.randint(100, 999)}",
                "event_type": random.choice(self.event_types),
                "page": random.choice(self.pages),
                "element": random.choice(["button", "link", "input", "dropdown", "checkbox"]),
                "timestamp": (datetime.utcnow() - timedelta(seconds=random.randint(0, 3600))).isoformat(),
                "coordinates": {
                    "x": random.randint(0, 1920),
                    "y": random.randint(0, 1080)
                }
            })
        return events
    
    def track_user_event(self, event: Dict) -> Dict:
        return {
            "event_id": str(uuid.uuid4()),
            "status": "tracked",
            "timestamp": datetime.utcnow().isoformat(),
            "event_data": event
        }
    
    def get_form_submission_stats(self) -> Dict:
        return {
            "total_submissions_today": random.randint(100, 500),
            "successful_submissions": random.randint(80, 95),
            "failed_submissions": random.randint(5, 20),
            "validation_errors": random.randint(10, 50),
            "avg_completion_time_seconds": random.uniform(30, 180),
            "abandonment_rate": random.uniform(0.1, 0.3),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_browser_fingerprints(self) -> List[Dict]:
        browsers = ["Chrome", "Firefox", "Safari", "Edge"]
        os_list = ["Windows", "macOS", "Linux", "iOS", "Android"]
        
        fingerprints = []
        for _ in range(random.randint(5, 15)):
            fingerprints.append({
                "fingerprint_id": str(uuid.uuid4()),
                "browser": random.choice(browsers),
                "browser_version": f"{random.randint(90, 120)}.0",
                "os": random.choice(os_list),
                "screen_resolution": random.choice(["1920x1080", "1366x768", "2560x1440", "1440x900"]),
                "timezone": random.choice(["America/New_York", "America/Chicago", "America/Los_Angeles"]),
                "language": "en-US",
                "plugins": random.randint(0, 10),
                "canvas_hash": f"hash_{random.randint(100000, 999999)}",
                "webgl_vendor": random.choice(["NVIDIA", "AMD", "Intel"]),
                "timestamp": datetime.utcnow().isoformat()
            })
        return fingerprints
