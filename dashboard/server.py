import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from pathlib import Path
import config

logger = logging.getLogger(__name__)

app = FastAPI(title="ATC AI Assist Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory pub-sub for broadcasting to clients
class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.message_cache = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Flush the recent history cache to new clients so they don't see an empty screen
        for msg in self.message_cache:
            try:
                await websocket.send_text(msg)
            except:
                pass

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    def _update_cache(self, msg: str):
        try:
            data = json.loads(msg)
            topic = data.get("topic")
            if topic == "state":
                import copy
                self.message_cache = [m for m in self.message_cache if json.loads(m).get("topic") != "state"]
                self.message_cache.append(msg)
            elif topic == "transcript":
                self.message_cache.append(msg)
                transcripts = [m for m in self.message_cache if json.loads(m).get("topic") == "transcript"]
                if len(transcripts) > 15:
                    self.message_cache.remove(transcripts[0])
            elif topic == "alert":
                self.message_cache.append(msg)
                alerts = [m for m in self.message_cache if json.loads(m).get("topic") == "alert"]
                if len(alerts) > 10:
                    self.message_cache.remove(alerts[0])
        except Exception as e:
            logger.error(f"Cache error: {e}")

    async def broadcast(self, message: str):
        self._update_cache(message)
        # Create a copy to gracefully handle disconnections during broadcast
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"WebSocket broadcast error: {e}")
                self.disconnect(connection)

manager = ConnectionManager()
_main_loop = None

def broadcast_sync(topic: str, data: dict):
    """
    Called from other threads to push data to the asyncio loop.
    Since main processing happens in background threads, we inject into the 
    FastAPI event loop.
    """
    global _main_loop
    if _main_loop is None:
        return
        
    msg = json.dumps({"topic": topic, "data": data})
    try:
        asyncio.run_coroutine_threadsafe(manager.broadcast(msg), _main_loop)
    except Exception as e:
        logger.error(f"Failed to schedule broadcast: {e}")

@app.get("/")
async def get_dashboard():
    # Load dashboard.html
    template_path = Path(__file__).parent / "templates" / "dashboard.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return HTMLResponse(html)
    except FileNotFoundError:
        return HTMLResponse("<h1>Dashboard Template Missing</h1>", status_code=404)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from the client in this one-way feed
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
