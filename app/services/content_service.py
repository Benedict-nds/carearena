"""Content service."""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.content import Lesson, Condition, ContentVersion
from app.schemas.content import LessonCreate, ConditionCreate, ContentVersionCreate


class ContentService:
    """Service for content operations."""
    
    @staticmethod
    def get_lesson(db: Session, lesson_id: int) -> Optional[Lesson]:
        """Get lesson by ID."""
        return db.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    @staticmethod
    def get_lessons(db: Session, skip: int = 0, limit: int = 100) -> List[Lesson]:
        """Get all lessons."""
        return db.query(Lesson).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_lesson(db: Session, lesson_data: LessonCreate) -> Lesson:
        """Create a new lesson."""
        lesson = Lesson(**lesson_data.dict())
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson
    
    @staticmethod
    def get_condition(db: Session, condition_id: int) -> Optional[Condition]:
        """Get condition by ID."""
        return db.query(Condition).filter(Condition.id == condition_id).first()
    
    @staticmethod
    def get_conditions(db: Session) -> List[Condition]:
        """Get all conditions."""
        return db.query(Condition).all()
    
    @staticmethod
    def create_condition(db: Session, condition_data: ConditionCreate) -> Condition:
        """Create a new condition."""
        condition = Condition(**condition_data.dict())
        db.add(condition)
        db.commit()
        db.refresh(condition)
        return condition
    
    @staticmethod
    def create_version(db: Session, version_data: ContentVersionCreate) -> ContentVersion:
        """Create a new content version."""
        version = ContentVersion(**version_data.dict())
        db.add(version)
        db.commit()
        db.refresh(version)
        return version

