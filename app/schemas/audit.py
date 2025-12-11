"""Audit schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogBase(BaseModel):
    """Base audit log schema."""
    action: str
    entity_type: str
    entity_id: Optional[int] = None
    user_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log."""
    timestamp: datetime = datetime.utcnow()


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""
    id: int
    timestamp: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True

