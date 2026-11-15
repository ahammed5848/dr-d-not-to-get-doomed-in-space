from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import json
import asyncio
from ..simulator import simulator

router = APIRouter(tags=["WebSocket Live Streaming"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()

# Hook simulator updates directly to manager broadcast
async def on_simulator_tick(payload: Dict[str, Any]):
    await manager.broadcast(payload)

simulator.add_listener(on_simulator_tick)

@router.websocket("/ws/live")
async def websocket_live_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send initial welcome state
    try:
        await websocket.send_json({
            "type": "CONNECTION_ESTABLISHED",
            "message": "Connected to Dr D High-Rate Telemetry Stream",
            "active_scenarios": simulator.get_active_scenarios_list(),
            "simulation_speed": simulator.speed
        })
        while True:
            # Keep connection alive & accept client commands (e.g. ping or speed adjustment)
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg.get("action") == "trigger_scenario":
                    simulator.trigger_scenario(
                        scenario_type=msg.get("scenario_type"),
                        astronaut_id=msg.get("astronaut_id"),
                        severity=msg.get("severity", "moderate")
                    )
            except Exception:
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
