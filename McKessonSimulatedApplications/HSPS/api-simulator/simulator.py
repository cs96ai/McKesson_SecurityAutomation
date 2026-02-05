import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class APISimulator:
    def __init__(self):
        self.active_sessions = 0
        self.total_requests = 0
        self.endpoints = [
            "/api/v1/prescriptions",
            "/api/v1/medications",
            "/api/v1/inventory",
            "/api/v1/orders",
            "/api/v1/patients"
        ]
        
        self.medications = [
            "Lisinopril", "Metformin", "Amlodipine", "Metoprolol", "Omeprazole",
            "Simvastatin", "Losartan", "Albuterol", "Gabapentin", "Hydrochlorothiazide",
            "Sertraline", "Montelukast", "Furosemide", "Atorvastatin", "Levothyroxine"
        ]
        
        self.locations = ["Pharmacy-Main", "Pharmacy-ER", "Pharmacy-ICU", "Central-Supply"]
    
    def generate_metrics(self) -> Dict:
        self.active_sessions = random.randint(50, 200)
        
        requests_by_endpoint = {}
        for endpoint in self.endpoints:
            requests_by_endpoint[endpoint] = random.randint(10, 100)
        
        response_times = {}
        for endpoint in self.endpoints:
            response_times[endpoint] = random.uniform(0.05, 0.5)
        
        error_rate = random.uniform(0.5, 5.0)
        
        return {
            "active_sessions": self.active_sessions,
            "requests_by_endpoint": requests_by_endpoint,
            "response_times": response_times,
            "error_rate": round(error_rate, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_prescriptions(self, patient_id: Optional[str], limit: int) -> List[Dict]:
        prescriptions = []
        for _ in range(min(limit, random.randint(1, 10))):
            prescriptions.append({
                "prescription_id": str(uuid.uuid4()),
                "patient_id": patient_id or f"PAT-{random.randint(10000, 99999)}",
                "medication": random.choice(self.medications),
                "dosage": f"{random.choice([5, 10, 20, 50, 100])}mg",
                "frequency": random.choice(["Once daily", "Twice daily", "Three times daily", "As needed"]),
                "prescriber": f"Dr. {random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones'])}",
                "prescribed_date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                "status": random.choice(["Active", "Filled", "Pending"])
            })
        return prescriptions
    
    def get_medications(self, search: Optional[str], limit: int) -> List[Dict]:
        medications = []
        med_list = self.medications if not search else [m for m in self.medications if search.lower() in m.lower()]
        
        for med in med_list[:limit]:
            medications.append({
                "medication_id": str(uuid.uuid4()),
                "name": med,
                "generic_name": med.lower(),
                "strength": f"{random.choice([5, 10, 20, 50, 100])}mg",
                "form": random.choice(["Tablet", "Capsule", "Liquid", "Injection"]),
                "manufacturer": random.choice(["Pfizer", "Merck", "GSK", "Novartis", "Roche"]),
                "ndc": f"{random.randint(10000, 99999)}-{random.randint(100, 999)}-{random.randint(10, 99)}"
            })
        return medications
    
    def get_inventory(self, location: Optional[str]) -> List[Dict]:
        inventory = []
        locations = [location] if location else self.locations
        
        for loc in locations:
            for _ in range(random.randint(5, 15)):
                inventory.append({
                    "item_id": str(uuid.uuid4()),
                    "medication": random.choice(self.medications),
                    "location": loc,
                    "quantity": random.randint(0, 500),
                    "reorder_level": random.randint(50, 100),
                    "expiry_date": (datetime.utcnow() + timedelta(days=random.randint(30, 365))).isoformat(),
                    "lot_number": f"LOT-{random.randint(100000, 999999)}"
                })
        return inventory
    
    def create_order(self, order: Dict) -> Dict:
        return {
            "order_id": str(uuid.uuid4()),
            "status": "Created",
            "created_at": datetime.utcnow().isoformat(),
            "estimated_completion": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
            "items": order.get("items", []),
            "total_items": len(order.get("items", []))
        }
    
    def get_patient(self, patient_id: str) -> Dict:
        return {
            "patient_id": patient_id,
            "name": f"Patient {random.randint(1000, 9999)}",
            "dob": (datetime.utcnow() - timedelta(days=random.randint(18*365, 80*365))).date().isoformat(),
            "allergies": random.sample(["Penicillin", "Sulfa", "Aspirin", "None"], k=random.randint(0, 2)),
            "active_prescriptions": random.randint(0, 5),
            "last_visit": (datetime.utcnow() - timedelta(days=random.randint(1, 90))).isoformat()
        }
    
    def get_api_stats(self) -> Dict:
        return {
            "total_requests_last_hour": random.randint(1000, 5000),
            "avg_response_time_ms": random.uniform(50, 200),
            "p95_response_time_ms": random.uniform(200, 500),
            "p99_response_time_ms": random.uniform(500, 1000),
            "error_rate_percent": random.uniform(0.5, 3.0),
            "active_api_keys": random.randint(20, 100),
            "rate_limited_requests": random.randint(0, 50),
            "cache_hit_ratio": random.uniform(0.6, 0.9),
            "timestamp": datetime.utcnow().isoformat()
        }
