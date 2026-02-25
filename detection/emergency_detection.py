import time
from typing import Dict, Any, List
import config

class EmergencyDetector:
    def __init__(self, aircraft_engine, ground_engine):
        self.aircraft_engine = aircraft_engine
        self.ground_engine = ground_engine
        
    def detect_emergencies(self) -> List[Dict[str, Any]]:
        alerts = []
        ac_snap = self.aircraft_engine.get_snapshot()
        gnd_snap = self.ground_engine.get_snapshot()
        
        for eid, ac in ac_snap.items():
            if ac["emergency_flag"]:
                alerts.append({
                    "alert_type": "EMERGENCY_DECLARED",
                    "severity": config.CONFLICT_SEVERITY_HIGH,
                    "entities": [eid],
                    "message": f"EMERGENCY declared for Aircraft {eid}. Simulating emergency dispatch.",
                    "timestamp": time.time()
                })
                
        for eid, v in gnd_snap.items():
             if v["emergency_flag"]:
                 alerts.append({
                    "alert_type": "EMERGENCY_DECLARED",
                    "severity": config.CONFLICT_SEVERITY_HIGH,
                    "entities": [eid],
                    "message": f"EMERGENCY declared for Vehicle {eid}. Simulating emergency dispatch.",
                    "timestamp": time.time()
                })
                 
        return alerts
