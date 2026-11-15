from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Threshold, User
from ..schemas import ThresholdResponse, ThresholdUpdate
from ..auth import require_role

router = APIRouter(prefix="/api/thresholds", tags=["Threshold Configuration"])

@router.get("", response_model=List[ThresholdResponse])
def get_thresholds(db: Session = Depends(get_db)):
    return db.query(Threshold).all()

@router.put("/{metric}", response_model=ThresholdResponse)
def update_threshold(
    metric: str,
    threshold_in: ThresholdUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "surgeon"]))
):
    th = db.query(Threshold).filter(Threshold.metric == metric).first()
    if not th:
        raise HTTPException(status_code=404, detail=f"Threshold metric '{metric}' not found.")

    new_w_low = threshold_in.warning_low if threshold_in.warning_low is not None else th.warning_low
    new_w_high = threshold_in.warning_high if threshold_in.warning_high is not None else th.warning_high
    new_c_low = threshold_in.critical_low if threshold_in.critical_low is not None else th.critical_low
    new_c_high = threshold_in.critical_high if threshold_in.critical_high is not None else th.critical_high

    # Edge-case boundary validation
    if new_w_low is not None and new_w_high is not None and new_w_low > new_w_high:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid boundary: warning_low ({new_w_low}) cannot exceed warning_high ({new_w_high})."
        )
    if new_c_low is not None and new_w_low is not None and new_c_low > new_w_low:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid boundary: critical_low ({new_c_low}) cannot exceed warning_low ({new_w_low})."
        )
    if new_c_high is not None and new_w_high is not None and new_c_high < new_w_high:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid boundary: critical_high ({new_c_high}) cannot be less than warning_high ({new_w_high})."
        )

    th.warning_low = threshold_in.warning_low
    th.warning_high = threshold_in.warning_high
    th.critical_low = threshold_in.critical_low
    th.critical_high = threshold_in.critical_high

    db.commit()
    db.refresh(th)
    return th
