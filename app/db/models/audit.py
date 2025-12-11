"""Audit log model."""

from sqlalchemy import Column, String, Integer, Text, JSON, DateTime
from app.db.base import BaseModel


class AuditLog(BaseModel):
    """Audit log model."""
    
    __tablename__ = "audit_logs"
    
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    timestamp = Column(DateTime, nullable=False)

