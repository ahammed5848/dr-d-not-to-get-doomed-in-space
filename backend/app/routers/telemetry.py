from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
import csv
import io

from ..database import get_db
from ..models import VitalReading, EnvironmentReading, Astronaut
from ..schemas import (
    VitalReadingCreate, VitalReadingResponse,
    EnvironmentReadingCreate, EnvironmentReadingResponse
)
from ..auth import get_current_user, require_role

router = APIRouter(prefix="/api", tags=["Telemetry Ingestion & Environment"])

@router.post("/telemetry", response_model=VitalReadingResponse)
def ingest_telemetry(
    vital_in: VitalReadingCreate,
    db: Session = Depends(get_db)
):
    """
    Direct ingestion endpoint for physical telemetry devices, space suit sensors,
    or external medical wearables.
    """
    astro = db.query(Astronaut).filter(Astronaut.id == vital_in.astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail=f"Astronaut ID {vital_in.astronaut_id} not found.")

    new_vital = VitalReading(
        astronaut_id=vital_in.astronaut_id,
        timestamp=vital_in.timestamp or datetime.now(timezone.utc),
        heart_rate=vital_in.heart_rate,
        hrv=vital_in.hrv,
        spo2=vital_in.spo2,
        bp_systolic=vital_in.bp_systolic,
        bp_diastolic=vital_in.bp_diastolic,
        core_temp=vital_in.core_temp,
        skin_temp=vital_in.skin_temp,
        respiratory_rate=vital_in.respiratory_rate,
        sleep_quality=vital_in.sleep_quality,
        stress_index=vital_in.stress_index,
        activity_level=vital_in.activity_level,
        fluid_shift_score=vital_in.fluid_shift_score,
        circadian_disruption_score=vital_in.circadian_disruption_score
    )
    db.add(new_vital)
    db.commit()
    db.refresh(new_vital)
    return new_vital

@router.post("/telemetry/batch", response_model=dict)
def ingest_telemetry_batch(
    readings: List[VitalReadingCreate],
    db: Session = Depends(get_db)
):
    """Batch ingestion endpoint for telemetry sync or wearable log dumps."""
    count = 0
    for v in readings:
        new_vital = VitalReading(
            astronaut_id=v.astronaut_id,
            timestamp=v.timestamp or datetime.now(timezone.utc),
            heart_rate=v.heart_rate,
            hrv=v.hrv,
            spo2=v.spo2,
            bp_systolic=v.bp_systolic,
            bp_diastolic=v.bp_diastolic,
            core_temp=v.core_temp,
            skin_temp=v.skin_temp,
            respiratory_rate=v.respiratory_rate,
            sleep_quality=v.sleep_quality,
            stress_index=v.stress_index,
            activity_level=v.activity_level,
            fluid_shift_score=v.fluid_shift_score,
            circadian_disruption_score=v.circadian_disruption_score
        )
        db.add(new_vital)
        count += 1
    db.commit()
    return {"status": "success", "ingested_count": count}

@router.post("/telemetry/csv", response_model=dict)
async def ingest_telemetry_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    CSV Telemetry Ingestion endpoint.
    Supports importing raw CSV biometric data files from external wearables or suit sensors.
    """
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    ingested = 0
    for row in reader:
        try:
            # Handle comment lines or headers
            if not row or not any(row.values()):
                continue
            astro_id = int(row.get("astronaut_id") or row.get("Astronaut ID") or 1)
            hr = float(row.get("heart_rate") or row.get("Heart Rate (bpm)") or 70.0)
            hrv = float(row.get("hrv") or row.get("HRV (ms)") or 60.0)
            spo2 = float(row.get("spo2") or row.get("SpO2 (%)") or 98.0)
            bp_sys = float(row.get("bp_systolic") or row.get("BP Systolic (mmHg)") or 120.0)
            bp_dia = float(row.get("bp_diastolic") or row.get("BP Diastolic (mmHg)") or 80.0)
            core_t = float(row.get("core_temp") or row.get("Core Temp (°C)") or 36.8)
            skin_t = float(row.get("skin_temp") or row.get("Skin Temp (°C)") or 33.5)
            resp = float(row.get("respiratory_rate") or row.get("Respiratory Rate") or 14.0)
            stress = float(row.get("stress_index") or row.get("Stress Index (0-100)") or 20.0)
            fluid_s = float(row.get("fluid_shift_score") or row.get("Fluid Shift Index") or 18.0)
            circ = float(row.get("circadian_disruption_score") or row.get("Circadian Disruption") or 14.0)
            act = row.get("activity_level") or row.get("Activity") or "REST"

            ts_str = row.get("timestamp") or row.get("Timestamp")
            ts = datetime.now(timezone.utc)
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str)
                except Exception:
                    pass

            v = VitalReading(
                astronaut_id=astro_id,
                timestamp=ts,
                heart_rate=hr,
                hrv=hrv,
                spo2=spo2,
                bp_systolic=bp_sys,
                bp_diastolic=bp_dia,
                core_temp=core_t,
                skin_temp=skin_t,
                respiratory_rate=resp,
                sleep_quality=85.0,
                stress_index=stress,
                activity_level=act,
                fluid_shift_score=fluid_s,
                circadian_disruption_score=circ
            )
            db.add(v)
            ingested += 1
        except Exception:
            continue

    db.commit()
    return {"status": "success", "filename": file.filename, "records_ingested": ingested}

@router.get("/environment", response_model=List[EnvironmentReadingResponse])
def get_environment(
    limit: int = Query(60, ge=1, le=500),
    db: Session = Depends(get_db)
):
    readings = db.query(EnvironmentReading).order_by(
        EnvironmentReading.timestamp.desc()
    ).limit(limit).all()
    readings.reverse()
    return readings

@router.post("/environment", response_model=EnvironmentReadingResponse)
def ingest_environment(
    env_in: EnvironmentReadingCreate,
    db: Session = Depends(get_db)
):
    new_env = EnvironmentReading(
        timestamp=env_in.timestamp or datetime.now(timezone.utc),
        co2_ppm=env_in.co2_ppm,
        o2_pct=env_in.o2_pct,
        cabin_temp_c=env_in.cabin_temp_c,
        humidity_pct=env_in.humidity_pct,
        cabin_pressure_kpa=env_in.cabin_pressure_kpa,
        noise_db=env_in.noise_db
    )
    db.add(new_env)
    db.commit()
    db.refresh(new_env)
    return new_env
