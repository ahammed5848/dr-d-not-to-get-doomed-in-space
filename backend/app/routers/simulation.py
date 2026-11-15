from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import csv
import io
from datetime import datetime, timezone

from ..database import get_db
from ..models import Astronaut, VitalReading, Alert
from ..schemas import ScenarioTriggerRequest, SpeedChangeRequest
from ..simulator import simulator

router = APIRouter(prefix="/api/simulation", tags=["Data Simulation Engine"])

@router.post("/scenario")
def trigger_scenario(request: ScenarioTriggerRequest):
    """
    Trigger dynamic medical and environmental emergencies for hackathon demo.
    Scenarios: co2_spike, eva_cardiac_stress, radiation_storm, sleep_deprivation,
    dehydration, sensor_failure, nominal (reset).
    """
    res = simulator.trigger_scenario(
        scenario_type=request.scenario_type,
        astronaut_id=request.astronaut_id,
        severity=request.severity or "moderate"
    )
    return res

@router.post("/speed")
def set_simulation_speed(request: SpeedChangeRequest):
    """Adjust simulation clock speed (1x real-time, 10x accelerated, 60x fast-forward)"""
    return simulator.set_speed(request.speed)

@router.get("/status")
def get_simulation_status():
    return {
        "speed": simulator.speed,
        "is_running": simulator.is_running,
        "tick_count": simulator.tick_count,
        "active_scenarios": simulator.get_active_scenarios_list(),
        "cabin_environment": {
            "co2_ppm": simulator.cabin_co2,
            "o2_pct": simulator.cabin_o2,
            "temp_c": simulator.cabin_temp,
            "pressure_kpa": simulator.cabin_pressure
        }
    }

@router.post("/reset")
def reset_simulation(db: Session = Depends(get_db)):
    """Reset all scenarios back to nominal parameters"""
    simulator.trigger_scenario("nominal")
    # Reset astronaut statuses to NOMINAL
    db.query(Astronaut).update({Astronaut.status: "NOMINAL"})
    # Mark active alerts as resolved
    db.query(Alert).filter(Alert.status == "ACTIVE").update({
        Alert.status: "RESOLVED",
        Alert.acknowledged_by: "System Reset"
    })
    db.commit()
    return {"status": "success", "message": "Simulation reset to nominal state."}

@router.post("/import-csv")
async def import_vitals_csv(
    file: UploadFile = File(...),
    astronaut_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Alternative data source: Import a CSV of recorded vitals from wearables or medical equipment.
    Columns expected: heart_rate, hrv, spo2, bp_systolic, bp_diastolic, core_temp, respiratory_rate
    """
    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    count = 0
    now = datetime.now(timezone.utc)
    for row in reader:
        try:
            vital = VitalReading(
                astronaut_id=astronaut_id,
                timestamp=now,
                heart_rate=float(row.get("heart_rate", 70.0)),
                hrv=float(row.get("hrv", 60.0)),
                spo2=float(row.get("spo2", 98.0)),
                bp_systolic=float(row.get("bp_systolic", 120.0)),
                bp_diastolic=float(row.get("bp_diastolic", 80.0)),
                core_temp=float(row.get("core_temp", 36.8)),
                skin_temp=float(row.get("skin_temp", 33.5)),
                respiratory_rate=float(row.get("respiratory_rate", 14.0)),
                sleep_quality=float(row.get("sleep_quality", 85.0)),
                stress_index=float(row.get("stress_index", 20.0)),
                activity_level=row.get("activity_level", "REST")
            )
            db.add(vital)
            count += 1
        except Exception:
            continue

    db.commit()
    return {"status": "success", "imported_rows": count, "astronaut_id": astronaut_id}
