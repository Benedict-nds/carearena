"""Tests for session creation and turn logging."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
from app.main import app
from app.db.models.conversation import ConversationSession, ConversationTurn, SessionStatus
from app.db.models.patient import Patient
from app.db.models.hospital import Hospital

client = TestClient(app)


@pytest.fixture
def test_patient(db: Session):
    """Create test patient."""
    hospital = Hospital(name="Test Hospital", code="TEST001")
    db.add(hospital)
    db.commit()
    
    patient = Patient(
        hospital_id=hospital.id,
        first_name="Test",
        last_name="Patient",
        phone_number="+233241234567"
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def test_create_session(db: Session, test_patient):
    """Test creating a conversation session."""
    session_data = {
        "patient_id": test_patient.id,
        "channel": "ivr",
        "started_at": datetime.utcnow().isoformat()
    }
    
    response = client.post("/api/v1/sessions/", json=session_data)
    assert response.status_code == 200 or response.status_code == 201
    # TODO: Assert response data


def test_add_turn_to_session(db: Session, test_patient):
    """Test adding a conversation turn to a session."""
    # Create session first
    session = ConversationSession(
        patient_id=test_patient.id,
        channel="ivr",
        status=SessionStatus.ACTIVE,
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    
    # Add turn
    turn = ConversationTurn(
        session_id=session.id,
        turn_number=1,
        role="user",
        user_input="Hello",
        assistant_response="Hi there!"
    )
    db.add(turn)
    db.commit()
    
    assert turn.session_id == session.id
    assert turn.turn_number == 1
    # TODO: Assert turn is properly linked


def test_get_session_turns(db: Session, test_patient):
    """Test getting all turns for a session."""
    # Create session with turns
    session = ConversationSession(
        patient_id=test_patient.id,
        channel="ivr",
        status=SessionStatus.ACTIVE,
        started_at=datetime.utcnow()
    )
    db.add(session)
    db.commit()
    
    for i in range(3):
        turn = ConversationTurn(
            session_id=session.id,
            turn_number=i + 1,
            role="user" if i % 2 == 0 else "assistant",
            user_input="Input" if i % 2 == 0 else None,
            assistant_response="Response" if i % 2 == 1 else None
        )
        db.add(turn)
    db.commit()
    
    response = client.get(f"/api/v1/sessions/{session.id}")
    assert response.status_code == 200
    # TODO: Assert turns are included in response
