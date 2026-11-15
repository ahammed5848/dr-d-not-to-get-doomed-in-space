from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from ..database import get_db
from ..models import Astronaut, VitalReading, Alert, User
from ..reports import generate_csv_report, generate_pdf_report
from ..auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports & Export"])

@router.get("/{astronaut_id}")
def get_health_report(
    astronaut_id: int,
    format: str = Query("pdf", pattern="^(csv|pdf)$"),
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "astronaut" and current_user.astronaut_id != astronaut_id:
        raise HTTPException(status_code=403, detail="Astronauts can only export their own report.")

    astro = db.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    vitals = db.query(VitalReading).filter(
        VitalReading.astronaut_id == astronaut_id,
        VitalReading.timestamp >= cutoff
    ).order_by(VitalReading.timestamp.asc()).all()

    alerts = db.query(Alert).filter(
        Alert.astronaut_id == astronaut_id,
        Alert.timestamp >= cutoff
    ).order_by(Alert.timestamp.desc()).all()

    filename_safe = astro.callsign.lower().replace(" ", "_")

    if format == "csv":
        csv_data = generate_csv_report(astro, vitals, alerts)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=dr_d_report_{filename_safe}.csv"}
        )
    else:
        pdf_bytes = generate_pdf_report(astro, vitals, alerts)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=dr_d_report_{filename_safe}.pdf"}
        )
