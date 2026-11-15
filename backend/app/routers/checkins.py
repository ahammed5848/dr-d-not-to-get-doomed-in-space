from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from ..database import get_db
from ..models import DailyCheckin, Astronaut, User
from ..schemas import DailyCheckinCreate, DailyCheckinResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/checkins", tags=["Daily Wellbeing Check-ins"])

@router.get("", response_model=List[DailyCheckinResponse])
def get_checkins(
    astronaut_id: Optional[int] = Query(None),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(DailyCheckin)
    if current_user.role == "astronaut" and current_user.astronaut_id:
        query = query.filter(DailyCheckin.astronaut_id == current_user.astronaut_id)
    elif astronaut_id:
        query = query.filter(DailyCheckin.astronaut_id == astronaut_id)

    return query.order_by(DailyCheckin.timestamp.desc()).limit(limit).all()

@router.post("", response_model=DailyCheckinResponse, status_code=status.HTTP_201_CREATED)
def submit_checkin(
    checkin_in: DailyCheckinCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_astro_id = checkin_in.astronaut_id
    if current_user.role == "astronaut" and current_user.astronaut_id:
        target_astro_id = current_user.astronaut_id

    astro = db.query(Astronaut).filter(Astronaut.id == target_astro_id).first()
    if not astro:
        raise HTTPException(status_code=404, detail="Astronaut not found")

    # Validate range
    if not (0 <= checkin_in.sleep_hours <= 24):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="sleep_hours must be between 0 and 24.")

    for field_name in ["sleep_quality_score", "physical_fatigue", "cognitive_fatigue", "mood_score", "muscle_soreness", "headache_score", "space_motion_sickness"]:
        val = getattr(checkin_in, field_name, None)
        if val is not None and not (1.0 <= val <= 10.0):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{field_name} must be within 1.0 to 10.0 scale.")

    now = datetime.now(timezone.utc)
    new_checkin = DailyCheckin(
        astronaut_id=target_astro_id,
        timestamp=now,
        date=now.strftime("%Y-%m-%d"),
        sleep_hours=checkin_in.sleep_hours,
        sleep_quality_score=checkin_in.sleep_quality_score,
        physical_fatigue=checkin_in.physical_fatigue,
        cognitive_fatigue=checkin_in.cognitive_fatigue,
        mood_score=checkin_in.mood_score,
        muscle_soreness=checkin_in.muscle_soreness,
        headache_score=checkin_in.headache_score,
        space_motion_sickness=checkin_in.space_motion_sickness,
        comments=checkin_in.comments
    )
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)
    return new_checkin
