from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app.db.schemas import StatsResponse

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)) -> StatsResponse:
    total_scans = db.scalar(select(func.count(models.Detection.id))) or 0
    scam_count = db.scalar(
        select(func.count(models.Detection.id)).where(models.Detection.is_scam.is_(True))
    ) or 0
    avg_confidence = db.scalar(select(func.avg(models.Detection.confidence))) or 0.0

    type_row = db.execute(
        select(models.Detection.scam_type, func.count(models.Detection.id).label("count"))
        .group_by(models.Detection.scam_type)
        .order_by(func.count(models.Detection.id).desc())
        .limit(1)
    ).first()
    most_common = type_row[0] if type_row else None

    scam_rate = (scam_count / total_scans) if total_scans else 0.0
    return StatsResponse(
        total_scans=total_scans,
        scam_rate=float(round(scam_rate, 4)),
        most_common_scam_type=most_common,
        average_confidence=float(round(avg_confidence, 4)),
    )
