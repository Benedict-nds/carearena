"""Consent management models."""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class ConsentType(str, enum.Enum):
    """Consent type enum."""
    IVR = "ivr"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    DATA_SHARING = "data_sharing"


class ConsentStatus(str, enum.Enum):
    """Consent status enum."""
    GRANTED = "granted"
    REVOKED = "revoked"
    PENDING = "pending"


class ConsentRecord(BaseModel):
    """Consent record model."""
    
    __tablename__ = "consent_records"
    
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    consent_type = Column(Enum(ConsentType), nullable=False)
    status = Column(Enum(ConsentStatus), default=ConsentStatus.PENDING)
    granted_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="consent_records")

