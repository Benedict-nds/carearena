"""Content schemas."""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ConditionBase(BaseModel):
    """Base condition schema."""
    name: str
    description: Optional[str] = None


class ConditionCreate(ConditionBase):
    """Schema for creating a condition."""
    pass


class ConditionResponse(ConditionBase):
    """Schema for condition response."""
    id: int
    
    class Config:
        from_attributes = True


class LessonBase(BaseModel):
    """Base lesson schema."""
    title: str
    content: str
    language: str = "en"
    order: int = 0
    metadata: Optional[Dict[str, Any]] = None


class LessonCreate(LessonBase):
    """Schema for creating a lesson."""
    condition_id: int


class LessonResponse(LessonBase):
    """Schema for lesson response."""
    id: int
    condition_id: int
    
    class Config:
        from_attributes = True


class ContentVersionBase(BaseModel):
    """Base content version schema."""
    version_number: str
    content: str
    change_log: Optional[str] = None


class ContentVersionCreate(ContentVersionBase):
    """Schema for creating a content version."""
    lesson_id: int


class ContentVersionResponse(ContentVersionBase):
    """Schema for content version response."""
    id: int
    lesson_id: int
    
    class Config:
        from_attributes = True

