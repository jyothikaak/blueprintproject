from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    cleaned_text: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    detection: Mapped["Detection"] = relationship(back_populates="message", uselist=False)
    feedback_items: Mapped[list["Feedback"]] = relationship(back_populates="message")


class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), nullable=False, unique=True)
    is_scam: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    scam_type: Mapped[str] = mapped_column(String(100), nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    message: Mapped["Message"] = relationship(back_populates="detection")
    reasons: Mapped[list["DetectionReason"]] = relationship(back_populates="detection", cascade="all, delete-orphan")


class DetectionReason(Base):
    __tablename__ = "detection_reasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    detection_id: Mapped[int] = mapped_column(ForeignKey("detections.id"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    detection: Mapped["Detection"] = relationship(back_populates="reasons")


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), nullable=False)
    user_feedback: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    message: Mapped["Message"] = relationship(back_populates="feedback_items")
