from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from ..database import get_db
from ..models import Alert, Astronaut, User
from ..schemas import AlertResponse, AlertUpdate
from ..auth import get_current_user, require_role
from ..research_data import get_context_for_metric

router = APIRouter(prefix="/api/alerts", tags=["Alerts & Notifications"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    astronaut_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None), # WARNING, CRITICAL
    status: Optional[str] = Query(None), # ACTIVE, ACKNOWLEDGED, RESOLVED
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Alert)

    # Scoping for astronauts
    if current_user.role == "astronaut" and current_user.astronaut_id:
        query = query.filter((Alert.astronaut_id == current_user.astronaut_id) | (Alert.astronaut_id.is_(None)))
    elif astronaut_id:
        query = query.filter(Alert.astronaut_id == astronaut_id)

    if severity:
        query = query.filter(Alert.threshold_level == severity.upper())
    if status:
        query = query.filter(Alert.status == status.upper())

    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()

    # Populate astronaut details for display
    results = []
    for a in alerts:
        resp = AlertResponse.model_validate(a)
        if a.astronaut:
            resp.astronaut_name = a.astronaut.name
            resp.astronaut_callsign = a.astronaut.callsign
        else:
            resp.astronaut_name = "Spacecraft Cabin"
            resp.astronaut_callsign = "HAB-ARES"
        resp.research_context = get_context_for_metric(a.metric)
        results.append(resp)

    return results

@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    update_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["surgeon", "admin"]))
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = update_data.status.upper()
    now_utc = datetime.now(timezone.utc)
    if update_data.notes:
        existing_notes = f"{alert.notes}\n" if alert.notes else ""
        alert.notes = f"{existing_notes}[{now_utc.strftime('%Y-%m-%d %H:%M UTC')} - {current_user.full_name}]: {update_data.notes}"

    if alert.status in ["ACKNOWLEDGED", "RESOLVED"]:
        alert.acknowledged_by = current_user.full_name
        alert.acknowledged_at = now_utc

    db.commit()
    db.refresh(alert)

    resp = AlertResponse.model_validate(alert)
    if alert.astronaut:
        resp.astronaut_name = alert.astronaut.name
        resp.astronaut_callsign = alert.astronaut.callsign
    else:
        resp.astronaut_name = "Spacecraft Cabin"
        resp.astronaut_callsign = "HAB-ARES"
    resp.research_context = get_context_for_metric(alert.metric)
    return resp
