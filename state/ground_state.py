from typing import Dict, Any

class GroundVehicle:
    def __init__(self, vehicle_id: str):
        self.vehicle_id = vehicle_id
        self.position = "unknown" # e.g. taxiway segment, runway, or platform
        self.route = []
        self.runway_entry_request = None
        self.clearance_state = "pending"
        self.emergency_flag = False
        
    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "position": self.position,
            "route": self.route,
            "runway_entry_request": self.runway_entry_request,
            "clearance_state": self.clearance_state,
            "emergency_flag": self.emergency_flag
        }

class GroundStateEngine:
    def __init__(self):
        self.vehicles: Dict[str, GroundVehicle] = {}
        
    def update_from_event(self, event: Dict[str, Any]):
        eid = event.get("entity_id", "UNKNOWN")
        
        # Skip aircrafts
        if event.get("entity_type") != "vehicle":
            return
            
        if eid not in self.vehicles:
             self.vehicles[eid] = GroundVehicle(eid)
             
        v = self.vehicles[eid]
        
        runway = event.get("runway")
        if runway:
            v.runway_entry_request = runway
            
        route = event.get("route", [])
        if route:
             for tw in route:
                 if tw not in v.route:
                     v.route.append(tw)
             # Assume position updates to the latest segment heard
             if len(v.route) > 0:
                 v.position = v.route[-1]
                 
        destination = event.get("destination")
        if destination:
             v.position = destination # Simplified: might immediately reflect reaching destination
             
        clearance_state = event.get("clearance_state")
        if clearance_state and clearance_state != "pending":
             v.clearance_state = clearance_state
             
        if event.get("emergency_flag"):
             v.emergency_flag = True
             
    def get_snapshot(self) -> Dict[str, Any]:
        return {eid: v.to_dict() for eid, v in self.vehicles.items()}
