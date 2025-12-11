"""Schedule preference model."""

from sqlalchemy import Column, String, Integer, ForeignKey, Time, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class SchedulePreference(BaseModel):
    """Schedule preference model for patient content delivery."""
    
    __tablename__ = "schedule_preferences"
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, unique=True)
    preferred_time = Column(Time, nullable=True)  # Preferred time of day for calls/messages
    preferred_days = Column(JSON, nullable=True)  # List of preferred days: ["monday", "wednesday", "friday"]
    channel_preference = Column(String, default="ivr")  # ivr, sms, whatsapp
    frequency = Column(String, default="weekly")  # daily, weekly, biweekly, monthly
    timezone = Column(String, default="Africa/Accra")
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="schedule_preferences")

