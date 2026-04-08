from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class DetectRequest(BaseModel):
    text: str = Field(min_length=3, max_length=12000)
    channel: str | None = Field(default=None, max_length=50)


class DetectResponse(BaseModel):
    message_id: int
    is_scam: bool
    confidence: float
    scam_type: str
    reasons: list[str]
    recommended_action: str
    created_at: datetime


class FeedbackRequest(BaseModel):
    message_id: int
    user_feedback: Literal["correct", "incorrect", "unsure"]


class FeedbackResponse(BaseModel):
    id: int
    message_id: int
    user_feedback: str
    created_at: datetime


class MessageSummary(BaseModel):
    message_id: int
    raw_text: str
    channel: str | None
    is_scam: bool
    confidence: float
    scam_type: str
    created_at: datetime


class MessageDetail(BaseModel):
    message_id: int
    raw_text: str
    cleaned_text: str
    channel: str | None
    is_scam: bool
    confidence: float
    scam_type: str
    reasons: list[str]
    recommended_action: str
    created_at: datetime


class StatsResponse(BaseModel):
    total_scans: int
    scam_rate: float
    most_common_scam_type: str | None
    average_confidence: float
