"""Patient model."""

from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Patient(BaseModel):
    """Patient model."""
    
    __tablename__ = "patients"
    
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    date_of_birth = Column(Date, nullable=True)
    language_preference = Column(String, default="en")  # en, tw, ga, ewe
    is_active = Column(Boolean, default=True)
    enrolled_at = Column(DateTime, nullable=True)
    
    # Relationships
    hospital = relationship("Hospital", back_populates="patients")
    sessions = relationship("ConversationSession", back_populates="patient")
    scheduled_calls = relationship("ScheduledCall", back_populates="patient")
    consent_records = relationship("ConsentRecord", back_populates="patient", cascade="all, delete-orphan")
    schedule_preferences = relationship("SchedulePreference", back_populates="patient", cascade="all, delete-orphan")

