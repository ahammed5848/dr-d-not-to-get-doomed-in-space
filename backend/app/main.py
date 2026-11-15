import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .seed import init_db
from .simulator import simulator
from .models import MissionInfo
from .schemas import MissionInfoResponse

from .routers import (
    auth, astronauts, telemetry, alerts,
    thresholds, checkins, simulation, reports, websocket, research
)

simulator_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database & Seed
    print("Dr D Backend starting up...")
    init_db()

    # Launch background simulation engine loop (unless in testing mode)
    global simulator_task
    import os
    if os.getenv("TESTING") != "1":
        simulator_task = asyncio.create_task(simulator.run_loop())

    yield

    # Shutdown
    print("Dr D Backend shutting down...")
    simulator.is_running = False
    if simulator_task:
        simulator_task.cancel()

app = FastAPI(
    title="Dr D — Astronaut Health Monitoring System API",
    description="Real-time biometric telemetry, anomaly detection, predictive health risk modeling, and mission-control alerts for deep space exploration.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(astronauts.router)
app.include_router(telemetry.router)
app.include_router(alerts.router)
app.include_router(thresholds.router)
app.include_router(checkins.router)
app.include_router(simulation.router)
app.include_router(reports.router)
app.include_router(websocket.router)
app.include_router(research.router)

@app.get("/api/mission", response_model=MissionInfoResponse, tags=["Mission Context"])
def get_mission_info(db: Session = Depends(get_db)):
    m = db.query(MissionInfo).first()
    if not m:
        return MissionInfoResponse(
            name=settings.MISSION_NAME,
            current_day=settings.MISSION_DAY,
            total_days=settings.TOTAL_MISSION_DAYS,
            phase=settings.MISSION_PHASE,
            distance_from_earth_km=settings.DISTANCE_FROM_EARTH_KM,
            comm_delay_sec=settings.COMM_DELAY_SECONDS,
            eva_status="STANDBY",
            active_scenarios=simulator.get_active_scenarios_list(),
            simulation_speed=simulator.speed
        )
    return MissionInfoResponse(
        name=m.name,
        current_day=m.current_day,
        total_days=m.total_days,
        phase=m.phase,
        distance_from_earth_km=m.distance_from_earth_km,
        comm_delay_sec=m.comm_delay_sec,
        eva_status=m.eva_status,
        active_scenarios=simulator.get_active_scenarios_list(),
        simulation_speed=simulator.speed
    )

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Dr D — Astronaut Health Monitoring System API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "mission": settings.MISSION_NAME,
        "phase": settings.MISSION_PHASE,
        "docs": "/docs",
        "websocket": "/ws/live"
    }

if __name__ == "__main__":
    import uvicorn
    raw_port = os.environ.get("PORT", "8000")
    try:
        port = int(raw_port)
    except (ValueError, TypeError):
        port = 8000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
