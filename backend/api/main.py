
import os
import traceback
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import run_in_threadpool

from backend.agents.orchestrator import run_war_room


app = FastAPI(
    title="SentinelOps Real-Time API",
    description="Live cybersecurity event monitoring and AI incident response",
    version="2.1.0"
)


# ==================================================
# CORS CONFIGURATION
# ==================================================

frontend_url = os.getenv("FRONTEND_URL", "")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if frontend_url:
    allowed_origins.append(frontend_url.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# WEBSOCKET CONNECTION MANAGER
# ==================================================

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):

        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(
                    jsonable_encoder(message)
                )
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


# ==================================================
# SIX-AGENT AI WAR ROOM
# ==================================================

async def execute_war_room(incident: dict):

    incident_id = incident.get("incident_id", "UNKNOWN")

    await manager.broadcast({
        "type": "war_room_started",
        "incident_id": incident_id,
        "message": "Six-agent AI investigation started.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    try:

        result = await run_in_threadpool(
            run_war_room,
            incident
        )

        await manager.broadcast({
            "type": "war_room_completed",
            "incident_id": incident_id,
            "data": jsonable_encoder(result),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    except Exception as error:

        print("WAR ROOM ERROR:", error)
        traceback.print_exc()

        await manager.broadcast({
            "type": "war_room_failed",
            "incident_id": incident_id,
            "error": str(error),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })


# ==================================================
# HOME
# ==================================================

@app.get("/")
async def home():

    return {
        "status": "online",
        "application": "SentinelOps",
        "message": "Real-Time Cybersecurity API is running"
    }


# ==================================================
# HEALTH CHECK
# ==================================================

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ==================================================
# RECEIVE LIVE EVENTS
# ==================================================

@app.post("/events")
async def receive_event(event: dict):

    await manager.broadcast({
        "type": "event",
        "data": event
    })

    return {
        "status": "received",
        "event_id": event.get("event_id"),
        "connected_dashboards": len(manager.active_connections)
    }


# ==================================================
# RECEIVE ALERT AND START AI INVESTIGATION
# ==================================================

@app.post("/alerts")
async def receive_alert(
    alert: dict,
    background_tasks: BackgroundTasks
):

    incident_id = alert.get(
        "incident_id",
        f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    )

    incident = {
        "incident_id": incident_id,
        "type": alert.get(
            "type",
            "Suspicious Login Activity"
        ),
        "attack_type": alert.get(
            "attack_type",
            "Possible Brute Force"
        ),
        "failed_attempts": alert.get(
            "failed_attempts",
            alert.get("attempts", 0)
        ),
        "time_window_minutes": alert.get(
            "time_window_minutes",
            1
        ),
        "target": alert.get(
            "target",
            alert.get("username", "Unknown Account")
        ),
        "unfamiliar_ip": alert.get(
            "unfamiliar_ip",
            True
        ),
        "successful_login": alert.get(
            "successful_login",
            False
        ),
        "source_ip": alert.get(
            "source_ip",
            "Not supplied"
        ),
        "environment": "Synthetic Simulation"
    }

    # Immediately notify connected dashboards.
    await manager.broadcast({
        "type": "threat_alert",
        "data": incident
    })

    # Execute all six agents after returning the HTTP response.
    background_tasks.add_task(
        execute_war_room,
        incident
    )

    return {
        "status": "accepted",
        "message": "Threat received. Six-agent AI War Room queued.",
        "incident_id": incident_id,
        "connected_dashboards": len(manager.active_connections)
    }


# ==================================================
# WEBSOCKET LIVE STREAM
# ==================================================

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:

        await websocket.send_json({
            "type": "connection",
            "message": "Connected to SentinelOps live event stream"
        })

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)
