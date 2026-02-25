import json
import logging
from typing import Dict, Any
import config

logger = logging.getLogger(__name__)

class EventStore:
    def __init__(self):
        self.events_file = config.EVENTS_LOG_PATH
        self.alerts_file = config.ALERTS_LOG_PATH
        
    def _append_to_file(self, filepath: str, data: Dict[str, Any]):
        try:
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            logger.error(f"Failed to write to {filepath}: {e}")
            
    def log_event(self, parsed_event: Dict[str, Any], raw_transcript: str = "", state_snapshot: Dict[str, Any] = None):
        log_entry = {
            "timestamp": parsed_event.get("timestamp"),
            "raw_transcript": raw_transcript,
            "parsed_event": parsed_event,
            "state_snapshot": state_snapshot or {}
        }
        self._append_to_file(self.events_file, log_entry)
        
    def log_alert(self, alert: Dict[str, Any]):
        self._append_to_file(self.alerts_file, alert)
