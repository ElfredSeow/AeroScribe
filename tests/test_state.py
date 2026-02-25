import pytest
import sys
import os

# Add root project path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from state.aircraft_state import AircraftStateEngine
from state.ground_state import GroundStateEngine

def test_aircraft_state_updates():
    engine = AircraftStateEngine()
    
    # 1. Initial hear
    engine.update_from_event({
        "entity_id": "Delta 45",
        "entity_type": "aircraft",
        "intent": "landing",
        "runway": "02",
        "route": [],
        "destination": None,
        "clearance_state": "pending",
        "emergency_flag": False
    })
    snap = engine.get_snapshot()
    assert "Delta 45" in snap
    assert snap["Delta 45"]["phase"] == "landing"
    assert snap["Delta 45"]["clearance_state"] == "pending"
    assert snap["Delta 45"]["runway"] == "02"
    
    # 2. Clearance granted
    engine.update_from_event({
        "entity_id": "Delta 45",
        "entity_type": "aircraft",
        "intent": "unknown", # Doesn't overwrite
        "runway": None,
        "route": [],
        "destination": None,
        "clearance_state": "granted",
        "emergency_flag": False
    })
    snap2 = engine.get_snapshot()
    assert snap2["Delta 45"]["phase"] == "landing" # Should retain
    assert snap2["Delta 45"]["clearance_state"] == "granted"

def test_vehicle_state_updates():
    engine = GroundStateEngine()
    engine.update_from_event({
        "entity_id": "Truck 1",
        "entity_type": "vehicle",
        "intent": "taxi",
        "runway": "09R",
        "route": ["Alpha"],
        "destination": None,
        "clearance_state": "pending",
        "emergency_flag": False
    })
    snap = engine.get_snapshot()
    assert snap["Truck 1"]["runway_entry_request"] == "09R"
    assert snap["Truck 1"]["position"] == "Alpha"
