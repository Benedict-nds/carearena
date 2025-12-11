"""Hospital model."""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Hospital(BaseModel):
    """Hospital model."""
    
    __tablename__ = "hospitals"
    
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False, index=True)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    
    # Relationships
    patients = relationship("Patient", back_populates="hospital")
    sync_logs = relationship("EnrollmentSyncLog", back_populates="hospital")

