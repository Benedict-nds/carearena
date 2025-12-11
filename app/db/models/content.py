"""Content models (lessons, conditions, versions)."""

from sqlalchemy import Column, String, Integer, Text, ForeignKey, JSON, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.base import BaseModel


class Condition(BaseModel):
    """Medical condition model."""
    
    __tablename__ = "conditions"
    
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    lessons = relationship("Lesson", back_populates="condition")


class LessonVersionStatus(str, enum.Enum):
    """Lesson version status enum."""
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Lesson(BaseModel):
    """Lesson model."""
    
    __tablename__ = "lessons"
    
    condition_id = Column(Integer, ForeignKey("conditions.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Current approved content
    language = Column(String, default="en")  # en, tw, ga, ewe
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    condition = relationship("Condition", back_populates="lessons")
    versions = relationship("LessonVersion", back_populates="lesson", cascade="all, delete-orphan")
    content_assets = relationship("ContentAsset", back_populates="lesson", cascade="all, delete-orphan")


class LessonVersion(BaseModel):
    """Lesson version model (draft → approved workflow)."""
    
    __tablename__ = "lesson_versions"
    
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    version_number = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(LessonVersionStatus), default=LessonVersionStatus.DRAFT)
    change_log = Column(Text, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="versions")
    approver = relationship("User", foreign_keys=[approved_by])


class ContentAsset(BaseModel):
    """Content asset model (audio, text files)."""
    
    __tablename__ = "content_assets"
    
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    asset_type = Column(String, nullable=False)  # audio, text, image
    file_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    language = Column(String, nullable=True)  # For multi-language assets
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="content_assets")

