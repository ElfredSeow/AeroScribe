import time
from typing import Dict, Any, List
import config

class ConflictDetector:
    def __init__(self, aircraft_engine, ground_engine):
        self.aircraft_engine = aircraft_engine
        self.ground_engine = ground_engine
        
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        alerts = []
        ac_snap = self.aircraft_engine.get_snapshot()
        gnd_snap = self.ground_engine.get_snapshot()
        
        # 1. Runway Conflict Detection
        # Group entities by runway mapping
        runway_occupants = {}
        for eid, ac in ac_snap.items():
            if ac["runway"] and ac["clearance_state"] == "granted":
                runway_occupants.setdefault(ac["runway"], []).append(eid)
                
        for eid, v in gnd_snap.items():
            if v["runway_entry_request"]:
                # If vehicle is on runway without clearance, it's a conflict
                if v["clearance_state"] != "granted":
                    alerts.append({
                        "alert_type": "RUNWAY_INCURSION_UNAUTHORIZED",
                        "severity": config.CONFLICT_SEVERITY_HIGH,
                        "entities": [eid],
                        "message": f"Vehicle {eid} is on/requesting runway {v['runway_entry_request']} without clearance.",
                        "timestamp": time.time()
                    })
                if v["clearance_state"] == "granted":
                    runway_occupants.setdefault(v["runway_entry_request"], []).append(eid)
                    
        # Check for multiple granted entities on same runway
        for rw, occupants in runway_occupants.items():
            if len(occupants) > 1:
                alerts.append({
                    "alert_type": "RUNWAY_CONFLICT",
                    "severity": config.CONFLICT_SEVERITY_HIGH,
                    "entities": occupants,
                    "message": f"Runway {rw} occupied/cleared for multiple entities: {', '.join(occupants)}",
                    "timestamp": time.time()
                })
                
        # 2. Taxiway Conflict
        taxiway_occupants = {}
        # Simple detection: if their latest route position matches
        for eid, ac in ac_snap.items():
            if ac["route"] and len(ac["route"]) > 0:
                tw = ac["route"][-1]
                taxiway_occupants.setdefault(tw, []).append(eid)
                
        for eid, v in gnd_snap.items():
            if v["position"] and v["position"] != "unknown":
                taxiway_occupants.setdefault(v["position"], []).append(eid)
                
        for tw, occupants in taxiway_occupants.items():
            if len(occupants) > 1:
                 alerts.append({
                    "alert_type": "TAXIWAY_CONFLICT",
                    "severity": config.CONFLICT_SEVERITY_MEDIUM,
                    "entities": occupants,
                    "message": f"Taxiway segment {tw} occupied by multiple entities: {', '.join(occupants)}",
                    "timestamp": time.time()
                })
                 
        # 3. Clearance Violation (Movement without clearance)
        for eid, ac in ac_snap.items():
            if ac["phase"] in ["taxi", "takeoff", "landing"] and ac["clearance_state"] == "pending":
                alerts.append({
                    "alert_type": "CLEARANCE_VIOLATION",
                    "severity": config.CONFLICT_SEVERITY_MEDIUM,
                    "entities": [eid],
                    "message": f"Aircraft {eid} intent {ac['phase']} detected without clearance.",
                    "timestamp": time.time()
                })
                
        for eid, v in gnd_snap.items():
             if len(v["route"]) > 0 and v["clearance_state"] == "pending":
                 alerts.append({
                    "alert_type": "CLEARANCE_VIOLATION",
                    "severity": config.CONFLICT_SEVERITY_MEDIUM,
                    "entities": [eid],
                    "message": f"Vehicle {eid} movement detected without clearance.",
                    "timestamp": time.time()
                })
                 
        return alerts
