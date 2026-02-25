import time
import logging
import threading
from typing import Callable

logger = logging.getLogger(__name__)

class RadioSimulator:
    def __init__(self, text_callback: Callable[[str], None], delay_between_calls=4.0):
        self.text_callback = text_callback
        self.delay = delay_between_calls
        self.is_running = False
        self._thread = None
        
        self.script = [
            # --- ROUTINE DEPARTURE (Pushback & Taxi) ---
            "Changi Ground, Singapore 318, aircraft type Boeing 777, stand F42, request pushback and start.",
            "Singapore 318, Changi Ground, pushback and start approved.",
            "Singapore 318, request taxi.",
            "Singapore 318, taxi to holding point Runway 02L via Alpha and Echo.",
            
            # --- ROUTINE ARRIVAL ---
            "Changi Tower, Scoot 421 is inbound for landing Runway 02L.",
            "Scoot 421, Changi Tower, wind 040 degrees 10 knots, Runway 02L, cleared to land.",
            
            # --- ROUTINE GROUND MOVEMENT ---
            "Ground, Sweeper 1 requesting to proceed via Charlie to Cargo.",
            "Sweeper 1, proceed via Charlie to Cargo, approved.",
            
            # --- ARRIVAL TAXI ---
            "Scoot 421, welcome to Changi, taxi to Platform 1 via Delta.",
            
            # --- RUNWAY INCURSION CONFLICT ---
            "Singapore 318, wind 050 degrees 12 knots, Runway 02L, cleared for takeoff.",
            "Ground, Sweeper 1 taxiing to Runway 02L for wildlife clearing.", 
            "Sweeper 1, negative! Hold position short of Runway 02L, traffic departing!",
            "Singapore 318, cancel takeoff clearance, I say again cancel takeoff clearance, hold position, vehicle on runway.",
            
            # --- RESOLVING INCURSION ---
            "Sweeper 1 holding short.",
            "Singapore 318, Runway 02L is clear, cleared for takeoff.",
            "Singapore 318, airborne.",
            
            # --- IN-FLIGHT EMERGENCY (PAN-PAN) ---
            "Changi Tower, Qantas 22, pan pan, pan pan, pan pan, medical passenger on board, requesting priority landing Runway 20R.",
            "Qantas 22, roger, priority landing approved for Runway 20R.",
            
            # --- HOLDING PATTERN DUE TO EMERGENCY ---
            "Cathay 711, hold short of Runway 20R, emergency traffic on approach.",
            
            # --- SEVERE GROUND EMERGENCY (MAYDAY) ---
            "Ground, Titan 9, mayday mayday mayday, engine fire, declaring emergency on Echo taxiway.",
            "Titan 9, emergency declared, dispatching fire rescue to Echo.",
        ]
        
    def start(self):
        if self.is_running: return
        self.is_running = True
        self._thread = threading.Thread(target=self._run_sim, daemon=True)
        self._thread.start()
        logger.info("Started scripted radio simulator.")
        
    def stop(self):
        self.is_running = False
        if self._thread:
             self._thread.join(timeout=2)
             
    def _run_sim(self):
        # Give UI a moment to connect
        time.sleep(3.0) 
        
        while self.is_running:
            for line in self.script:
                if not self.is_running: break
                
                logger.info(f"SIMULATOR 📡 : {line}")
                self.text_callback(line)
                
                time.sleep(self.delay)
            
            if self.is_running:
                logger.info("Restarting simulator script loop in 2s...")
                time.sleep(2.0)
                
        logger.info("End of simulator script.")
