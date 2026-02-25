import pytest
import sys
import os

# Add root project path so 'import audio...' works during pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio.atc_parser import ATCParser
import config

@pytest.fixture
def parser():
    return ATCParser(config=config.AIRPORT_LAYOUT)

def test_parse_taxi(parser):
    res = parser.parse("Spartan 1, taxi to Runway 09L via Alpha")
    assert res["entity_id"] == "Spartan 1"
    assert res["entity_type"] == "vehicle"
    assert res["intent"] == "taxi"
    assert "Alpha" in res["route"]
    assert res["runway"] == "09L"
    
def test_parse_landing(parser):
    res = parser.parse("Delta 45, cleared to land Runway 02")
    assert res["entity_id"] == "Delta 45"
    assert res["entity_type"] == "aircraft"
    assert res["intent"] == "landing"
    assert res["clearance_state"] == "granted"
    assert res["runway"] == "02"

def test_parse_emergency(parser):
    res = parser.parse("Mayday mayday, AC 123 engine failure")
    assert res["entity_id"] == "Ac 123"
    assert res["emergency_flag"] == True
    assert res["intent"] == "emergency"
