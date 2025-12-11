"""Schedule schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class ScheduleBase(BaseModel):
    """Base schedule schema."""
    scheduled_time: datetime
    channel: str = "voice"
    lesson_id: Optional[int] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ScheduleCreate(ScheduleBase):
    """Schema for creating a schedule."""
    patient_id: int


class ScheduleUpdate(BaseModel):
    """Schema for updating a schedule."""
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None
    channel: Optional[str] = None
    lesson_id: Optional[int] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None


class ScheduleResponse(ScheduleBase):
    """Schema for schedule response."""
    id: int
    patient_id: int
    status: str
    
    class Config:
        from_attributes = True

