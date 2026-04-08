from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app.db.schemas import MessageDetail, MessageSummary

router = APIRouter()


@router.get("/messages", response_model=list[MessageSummary])
def list_messages(db: Session = Depends(get_db)) -> list[MessageSummary]:
    stmt = (
        select(models.Message, models.Detection)
        .join(models.Detection, models.Detection.message_id == models.Message.id)
        .order_by(models.Message.created_at.desc())
    )
    rows = db.execute(stmt).all()
    return [
        MessageSummary(
            message_id=message.id,
            raw_text=message.raw_text,
            channel=message.channel,
            is_scam=detection.is_scam,
            confidence=float(round(detection.confidence, 4)),
            scam_type=detection.scam_type,
            created_at=message.created_at,
        )
        for message, detection in rows
    ]


@router.get("/messages/{message_id}", response_model=MessageDetail)
def get_message(message_id: int, db: Session = Depends(get_db)) -> MessageDetail:
    message = db.get(models.Message, message_id)
    if message is None or message.detection is None:
        raise HTTPException(status_code=404, detail="message not found")

    return MessageDetail(
        message_id=message.id,
        raw_text=message.raw_text,
        cleaned_text=message.cleaned_text,
        channel=message.channel,
        is_scam=message.detection.is_scam,
        confidence=float(round(message.detection.confidence, 4)),
        scam_type=message.detection.scam_type,
        reasons=[item.reason for item in message.detection.reasons],
        recommended_action=message.detection.recommended_action,
        created_at=message.created_at,
    )
