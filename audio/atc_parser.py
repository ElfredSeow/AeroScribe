import re
import time
from typing import Dict, Any

class ATCParser:
    def __init__(self, config=None):
        self.config = config or {}
        self.emergency_keywords = ["mayday", "pan pan", "fire", "medical", "engine failure", "declared emergency"]
        self.intents = {
            "taxi": ["taxi", "taxiing", "taxing"],
            "landing": ["cleared to land", "landing", "inbound", "touchdown"],
            "takeoff": ["cleared for takeoff", "takeoff", "taking off", "airborne"],
            "hold": ["hold position", "hold short", "holding"],
            "emergency": self.emergency_keywords
        }
        
    def parse(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # 1. Detect Emergency
        emergency_flag = any(kw in text_lower for kw in self.emergency_keywords)
        
        # 2. Extract Intent
        intent = "unknown"
        if emergency_flag:
            intent = "emergency"
        else:
            for k, v_list in self.intents.items():
                if any(kw in text_lower for kw in v_list):
                    intent = k
                    break
        
        # 3. Extract Clearance State
        clearance_state = "pending"
        if "cleared" in text_lower or "approved" in text_lower or "proceed" in text_lower:
            clearance_state = "granted"
            
        # 4. Extract Route (Taxiways)
        taxiways = []
        if self.config and "taxiways" in self.config:
            for tw in self.config["taxiways"]:
                if tw.lower() in text_lower:
                    taxiways.append(tw)
        else:
            # Fallback regex for common phonetic alphabets
            matches = re.findall(r'\b(alpha|bravo|charlie|delta|echo|foxtrot)\b', text_lower)
            taxiways = [m.capitalize() for m in set(matches)]
            
        # 5. Extract Runway
        runway = None
        if self.config and "runways" in self.config:
            for rw in self.config["runways"]:
                rw_variants = [rw.lower(), rw.replace("L", " left").replace("R", " right").lower()]
                if any(v in text_lower for v in rw_variants):
                    runway = rw
                    break
        if not runway:
            r_match = re.search(r'runway\s*([\d]{1,2}[lr]?)', text_lower)
            if r_match:
                runway = r_match.group(1).upper()
                
        # 6. Extract Destination
        destination = None
        if self.config and "platforms" in self.config:
            for plat in self.config["platforms"]:
                if plat.lower() in text_lower:
                    destination = plat
                    break
        if not destination:
            d_match = re.search(r'platform\s*(\d+)', text_lower)
            if d_match:
                destination = f"Platform {d_match.group(1)}"
        if not destination and "cargo" in text_lower:
            destination = "Cargo"
                
        # 7. Extract Entity
        entity_id = "UNKNOWN"
        entity_type = "unknown"
        
        # Look for identifiers like "Spartan 1", "AC 123", "Delta 45"
        entity_match = re.search(r'\b([a-z]+\s*\d{1,4})\b', text_lower)
        if entity_match:
            ent = entity_match.group(1).title()
            entity_id = ent
            if "vehicle" in ent.lower() or "spartan" in ent.lower() or "truck" in ent.lower():
                entity_type = "vehicle"
            else:
                entity_type = "aircraft"
        
        return {
            "entity_id": entity_id,
            "entity_type": entity_type,
            "intent": intent,
            "route": taxiways,
            "destination": destination,
            "runway": runway,
            "clearance_state": clearance_state,
            "emergency_flag": emergency_flag,
            "timestamp": time.time(),
            "confidence_score": 0.85 # Mock score for rule-based matching
        }
