import pytest
import sys
import os

# Add root project path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from state.aircraft_state import AircraftStateEngine
from state.ground_state import GroundStateEngine
from detection.conflict_detection import ConflictDetector

def test_runway_incursion():
    ac_eng = AircraftStateEngine()
    gnd_eng = GroundStateEngine()
    detector = ConflictDetector(ac_eng, gnd_eng)
    
    ac_eng.update_from_event({
        "entity_id": "Delta 45", "entity_type": "aircraft",
        "intent": "landing", "runway": "02", "route": [], "destination": None,
        "clearance_state": "granted", "emergency_flag": False
    })
    
    gnd_eng.update_from_event({
        "entity_id": "Spartan 1", "entity_type": "vehicle",
        "intent": "taxi", "runway": "02", "route": [], "destination": None,
        "clearance_state": "pending", "emergency_flag": False
    })
    
    alerts = detector.detect_conflicts()
    assert any(a["alert_type"] == "RUNWAY_INCURSION_UNAUTHORIZED" for a in alerts)
    
def test_taxiway_conflict():
    ac_eng = AircraftStateEngine()
    gnd_eng = GroundStateEngine()
    detector = ConflictDetector(ac_eng, gnd_eng)
    
    ac_eng.update_from_event({
        "entity_id": "AC123", "entity_type": "aircraft",
        "intent": "taxi", "runway": None, "route": ["Alpha"], "destination": None,
        "clearance_state": "granted", "emergency_flag": False
    })
    
    gnd_eng.update_from_event({
        "entity_id": "Truck 1", "entity_type": "vehicle",
        "intent": "taxi", "runway": None, "route": ["Alpha"], "destination": None,
        "clearance_state": "granted", "emergency_flag": False
    })
    
    alerts = detector.detect_conflicts()
    assert any(a["alert_type"] == "TAXIWAY_CONFLICT" for a in alerts)
