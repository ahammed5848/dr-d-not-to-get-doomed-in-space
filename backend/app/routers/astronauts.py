from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone, timedelta

from ..database import get_db
from ..models import (
    Astronaut, VitalReading, Alert, MedicalNote,
    EnvironmentReading, User, RiskSnapshot
)
from ..schemas import (
    AstronautResponse, VitalReadingResponse, RiskAssessmentResponse,
    ForecastResponse, MedicalNoteCreate, MedicalNoteResponse
)
from ..auth import get_current_user, require_role
from ..analytics import analytics_engine
from ..advisor import advisor_engine

router = APIRouter(prefix="/api/astronauts", tags=["Astronauts"])

@router.get("", response_model=List[AstronautResponse])
def get_astronauts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Astronaut)
    # Role-based scoping: Astronaut only sees themselves; Surgeon & Admin see all
    if current_user.role == "astronaut" and current_user.astronaut_id:
        query = query.filter(Astronaut.id == current_user.astronaut_id)
    
    astronauts = query.all()
    results = []
    for astro in astronauts:
        latest = db.query(VitalReading).filter(
            VitalReading.astronaut_id == astro.id
        ).order_by(VitalReading.timestamp.desc()).first()

        latest_dict = None
        if latest:
            latest_dict = {
                "heart_rate": latest.heart_rate,
                "hrv": latest.hrv,
                "spo2": latest.spo2,
                "bp_systolic": latest.bp_systolic,
                "bp_diastolic": latest.bp_diastolic,
                "core_temp": latest.core_temp,
                "skin_temp": latest.skin_temp,
                "respiratory_rate": latest.respiratory_rate,
                "sleep_quality": latest.sleep_quality,
                "stress_index": latest.stress_index,
                "activity_level": latest.activity_level,
                "timestamp": latest.timestamp.isoformat()
            }

        latest_risk = db.query(RiskSnapshot).filter(
            RiskSnapshot.astronaut_id == astro.id
        ).order_by(RiskSnapshot.timestamp.desc()).first()

        alerts_count = db.query(Alert).filter(
            Alert.astronaut_id == astro.id,
            Alert.status == "ACTIVE"
        ).count()

        resp = AstronautResponse.model_validate(astro)
        resp.latest_vitals = latest_dict
        resp.current_risk_score = latest_risk.composite_risk if latest_risk else 12.0
        resp.active_alerts_count = alerts_count
        results.append(resp)

    return results

@router.get("/{astronaut_id}", response_model=AstronautResponse)
def get_astronaut(
    astronaut_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view their own telemetry record.")

    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    latest = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astro.id
    ).order_by(VitalReading.timestamp.desc()).first()

    latest_dict = None
    if latest:
        latest_dict = {
            "heart_rate": latest.heart_rate,
            "hrv": latest.hrv,
            "spo2": latest.spo2,
            "bp_systolic": latest.bp_systolic,
            "bp_diastolic": latest.bp_diastolic,
            "core_temp": latest.core_temp,
            "skin_temp": latest.skin_temp,
            "respiratory_rate": latest.respiratory_rate,
            "sleep_quality": latest.sleep_quality,
            "stress_index": latest.stress_index,
            "activity_level": latest.activity_level,
            "timestamp": latest.timestamp.isoformat()
        }

    latest_risk = db.query(RiskSnapshot).filter(
        RiskSnapshot.astronaut_id == astro.id
    ).order_by(RiskSnapshot.timestamp.desc()).first()

    alerts_count = db.query(Alert).filter(
        Alert.astronaut_id == astro.id,
        Alert.status == "ACTIVE"
    ).count()

    resp = AstronautResponse.model_validate(astro)
    resp.latest_vitals = latest_dict
    resp.current_risk_score = latest_risk.composite_risk if latest_risk else 12.0
    resp.active_alerts_count = alerts_count
    return resp

@router.get("/{astronaut_id}/vitals", response_model=List[VitalReadingResponse])
def get_astronaut_vitals(
    astronaut_id: int,
    limit: int = Query(60, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view their own telemetry.")

    vitals = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astronaut_id
    ).order_by(VitalReading.timestamp.desc()).limit(limit).all()

    # Return chronological order for charts
    vitals.reverse()
    return vitals

@router.get("/{astronaut_id}/risk", response_model=RiskAssessmentResponse)
def get_astronaut_risk(
    astronaut_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view their own risk profile.")

    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    latest_vitals = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astronaut_id
    ).order_by(VitalReading.timestamp.desc()).first()

    latest_env = db.query(EnvironmentReading).order_by(
        EnvironmentReading.timestamp.desc()
    ).first()

    vitals_dict = {
        "heart_rate": latest_vitals.heart_rate if latest_vitals else 70.0,
        "hrv": latest_vitals.hrv if latest_vitals else 60.0,
        "spo2": latest_vitals.spo2 if latest_vitals else 98.0,
        "bp_systolic": latest_vitals.bp_systolic if latest_vitals else 120.0,
        "bp_diastolic": latest_vitals.bp_diastolic if latest_vitals else 80.0,
        "core_temp": latest_vitals.core_temp if latest_vitals else 36.8,
        "respiratory_rate": latest_vitals.respiratory_rate if latest_vitals else 14.0,
        "stress_index": latest_vitals.stress_index if latest_vitals else 20.0,
        "sleep_quality": latest_vitals.sleep_quality if latest_vitals else 85.0,
        "circadian_disruption_score": latest_vitals.circadian_disruption_score if latest_vitals else 15.0
    }
    baseline_dict = {
        "baseline_hr": astro.baseline_hr,
        "baseline_temp": astro.baseline_temp
    }
    env_dict = {
        "co2_ppm": latest_env.co2_ppm if latest_env else 520.0,
        "cabin_pressure_kpa": latest_env.cabin_pressure_kpa if latest_env else 101.3,
        "o2_pct": latest_env.o2_pct if latest_env else 21.0
    }

    risk_eval = analytics_engine.compute_composite_risk(vitals_dict, baseline_dict, env_dict)
    return RiskAssessmentResponse(
        astronaut_id=astronaut_id,
        composite_risk_score=risk_eval["composite_risk_score"],
        risk_level=risk_eval["risk_level"],
        factors=risk_eval["factors"],
        summary_explanation=risk_eval["summary_explanation"],
        recommended_action=risk_eval["recommended_action"]
    )

@router.get("/{astronaut_id}/forecast", response_model=ForecastResponse)
def get_astronaut_forecast(
    astronaut_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view their own forecast.")

    vitals = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astronaut_id
    ).order_by(VitalReading.timestamp.desc()).limit(20).all()

    if not vitals:
        raise HTTPException(status_code=400, detail="Insufficient vitals history for forecasting")

    vitals.reverse()

    # Key metrics forecast
    hr_vals = [v.heart_rate for v in vitals]
    spo2_vals = [v.spo2 for v in vitals]
    temp_vals = [v.core_temp for v in vitals]

    metrics_forecast = {
        "heart_rate": analytics_engine.forecast_metric(
            hr_vals, "heart_rate", hr_vals[-1], "bpm", warn_th=100.0, crit_th=125.0
        ),
        "spo2": analytics_engine.forecast_metric(
            spo2_vals, "spo2", spo2_vals[-1], "%", warn_th=95.0, crit_th=91.0
        ),
        "core_temp": analytics_engine.forecast_metric(
            temp_vals, "core_temp", temp_vals[-1], "°C", warn_th=37.8, crit_th=38.6
        )
    }

    return ForecastResponse(
        astronaut_id=astronaut_id,
        generated_at=datetime.now(timezone.utc),
        forecast_minutes=30,
        metrics=metrics_forecast
    )

@router.get("/{astronaut_id}/advisor")
def get_astronaut_advisor_recommendations(
    astronaut_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view their own clinical recommendations.")

    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    latest_v = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astronaut_id
    ).order_by(VitalReading.timestamp.desc()).first()

    latest_env = db.query(EnvironmentReading).order_by(
        EnvironmentReading.timestamp.desc()
    ).first()

    vitals_dict = {
        "heart_rate": latest_v.heart_rate if latest_v else 70.0,
        "spo2": latest_v.spo2 if latest_v else 98.0,
        "bp_systolic": latest_v.bp_systolic if latest_v else 120.0,
        "bp_diastolic": latest_v.bp_diastolic if latest_v else 80.0,
        "core_temp": latest_v.core_temp if latest_v else 36.8,
        "stress_index": latest_v.stress_index if latest_v else 20.0,
        "activity_level": latest_v.activity_level if latest_v else "REST",
        "circadian_disruption_score": latest_v.circadian_disruption_score if latest_v else 15.0
    }
    baseline_dict = {"baseline_hr": astro.baseline_hr, "baseline_temp": astro.baseline_temp}
    env_dict = {"co2_ppm": latest_env.co2_ppm if latest_env else 520.0}

    recs = advisor_engine.generate_recommendations(astro.name, vitals_dict, baseline_dict, env_dict)
    return {"astronaut_id": astronaut_id, "recommendations": recs}

@router.get("/{astronaut_id}/notes", response_model=List[MedicalNoteResponse])
def get_medical_notes(
    astronaut_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only view notes pertaining to their own profile.")

    notes = db.query(MedicalNote).filter(
        MedicalNote.astronaut_id == astronaut_id
    ).order_by(MedicalNote.timestamp.desc()).all()
    return notes

@router.post("/{astronaut_id}/notes", response_model=MedicalNoteResponse)
def add_medical_note(
    astronaut_id: int,
    note_in: MedicalNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["surgeon", "admin"]))
):
    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    new_note = MedicalNote(
        astronaut_id=astronaut_id,
        author_id=current_user.id,
        author_name=current_user.full_name,
        category=note_in.category,
        note_text=note_in.note_text,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note
