from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db
from app.db.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter()


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)) -> FeedbackResponse:
    message = db.get(models.Message, payload.message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="message_id not found")

    feedback = models.Feedback(message_id=payload.message_id, user_feedback=payload.user_feedback)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return FeedbackResponse(
        id=feedback.id,
        message_id=feedback.message_id,
        user_feedback=feedback.user_feedback,
        created_at=feedback.created_at,
    )
