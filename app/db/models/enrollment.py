"""Enrollment sync log model."""

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Integer as Int, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class SyncStatus(str, enum.Enum):
    """Sync status enum."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EnrollmentSyncLog(BaseModel):
    """Enrollment sync log for hospital CSV uploads."""
    
    __tablename__ = "enrollment_sync_logs"
    
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    filename = Column(String, nullable=False)
    total_rows = Column(Int, nullable=False)
    imported_count = Column(Int, default=0)
    skipped_count = Column(Int, default=0)
    error_count = Column(Int, default=0)
    status = Column(Enum(SyncStatus), default=SyncStatus.PENDING)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_details = Column(JSON, nullable=True)  # List of errors with row numbers
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    hospital = relationship("Hospital", back_populates="sync_logs")

