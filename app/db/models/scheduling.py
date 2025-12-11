"""Scheduling models."""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum, Boolean, JSON
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class CallStatus(str, enum.Enum):
    """Call status enum."""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    NO_ANSWER = "no_answer"
    BUSY = "busy"


class ScheduledCall(BaseModel):
    """Scheduled call model."""
    
    __tablename__ = "scheduled_calls"
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(Enum(CallStatus), default=CallStatus.PENDING)
    channel = Column(String, default="ivr")  # ivr, whatsapp, sms
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="scheduled_calls")

