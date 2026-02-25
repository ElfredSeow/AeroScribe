from typing import Dict, Any

class Aircraft:
    def __init__(self, callsign: str):
        self.callsign = callsign
        self.phase = "unknown" # taxi, landing, takeoff, hold, etc.
        self.runway = None
        self.route = []
        self.destination = None
        self.clearance_state = "pending"
        self.emergency_flag = False
        
    def to_dict(self):
        return {
            "callsign": self.callsign,
            "phase": self.phase,
            "runway": self.runway,
            "route": self.route,
            "destination": self.destination,
            "clearance_state": self.clearance_state,
            "emergency_flag": self.emergency_flag
        }

class AircraftStateEngine:
    def __init__(self):
        self.aircrafts: Dict[str, Aircraft] = {}
        
    def update_from_event(self, event: Dict[str, Any]):
        eid = event.get("entity_id", "UNKNOWN")
        
        # Skip vehicles
        if event.get("entity_type") == "vehicle":
            return
            
        if eid not in self.aircrafts:
             self.aircrafts[eid] = Aircraft(eid)
             
        ac = self.aircrafts[eid]
        
        intent = event.get("intent", "unknown")
        if intent != "unknown":
            ac.phase = intent
            
        runway = event.get("runway")
        if runway:
            ac.runway = runway
            
        route = event.get("route", [])
        if route:
            # Append newly heard taxiways to the route
            for tw in route:
                if tw not in ac.route:
                     ac.route.append(tw)
                     
        destination = event.get("destination")
        if destination:
             ac.destination = destination
             
        clearance_state = event.get("clearance_state")
        if clearance_state and clearance_state != "pending":
             ac.clearance_state = clearance_state
             
        if event.get("emergency_flag"):
             ac.emergency_flag = True
             
    def get_snapshot(self) -> Dict[str, Any]:
        return {eid: ac.to_dict() for eid, ac in self.aircrafts.items()}
