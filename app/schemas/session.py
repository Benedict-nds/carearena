"""Session schemas."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class MessageBase(BaseModel):
    """Base message schema."""
    role: str
    content: str
    audio_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    session_id: int


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    """Base session schema."""
    channel: str
    metadata: Optional[Dict[str, Any]] = None


class SessionCreate(SessionBase):
    """Schema for creating a session."""
    patient_id: int


class SessionResponse(SessionBase):
    """Schema for session response."""
    id: int
    patient_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

