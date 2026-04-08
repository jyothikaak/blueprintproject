from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import DetectRequest, DetectResponse
from app.services.detection_service import analyze_and_store

router = APIRouter()


@router.post("/detect", response_model=DetectResponse)
def detect(payload: DetectRequest, db: Session = Depends(get_db)) -> DetectResponse:
    return analyze_and_store(db=db, raw_text=payload.text, channel=payload.channel)
