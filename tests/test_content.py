"""Tests for content CRUD operations."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.models.content import Lesson, Condition, LessonVersion, LessonVersionStatus
from app.schemas.content import LessonCreate, ConditionCreate

client = TestClient(app)


@pytest.fixture
def test_condition(db: Session):
    """Create test condition."""
    condition = Condition(name="Preeclampsia", description="Preeclampsia education")
    db.add(condition)
    db.commit()
    db.refresh(condition)
    return condition


def test_create_lesson(db: Session, test_condition):
    """Test creating a lesson."""
    lesson_data = LessonCreate(
        condition_id=test_condition.id,
        title="Introduction to Preeclampsia",
        content="Preeclampsia is a condition...",
        language="en"
    )
    
    response = client.post("/api/v1/content/lessons", json=lesson_data.dict())
    assert response.status_code == 200 or response.status_code == 201
    # TODO: Assert response data


def test_get_lessons(db: Session, test_condition):
    """Test getting lessons."""
    response = client.get("/api/v1/content/lessons")
    assert response.status_code == 200
    # TODO: Assert response data


def test_lesson_version_workflow(db: Session, test_condition):
    """Test lesson version draft → approved workflow."""
    # Create lesson
    lesson = Lesson(
        condition_id=test_condition.id,
        title="Test Lesson",
        content="Initial content"
    )
    db.add(lesson)
    db.commit()
    
    # Create draft version
    draft_version = LessonVersion(
        lesson_id=lesson.id,
        version_number="1.0",
        content="Updated content",
        status=LessonVersionStatus.DRAFT
    )
    db.add(draft_version)
    db.commit()
    
    # Approve version
    draft_version.status = LessonVersionStatus.APPROVED
    db.commit()
    
    assert draft_version.status == LessonVersionStatus.APPROVED
    # TODO: Assert lesson content is updated


def test_get_conditions(db: Session):
    """Test getting conditions."""
    response = client.get("/api/v1/content/conditions")
    assert response.status_code == 200
    # TODO: Assert response data
