"""Tests for schedule preference logic."""

import pytest
from datetime import time
from sqlalchemy.orm import Session
from app.db.models.schedule_preference import SchedulePreference
from app.db.models.patient import Patient
from app.db.models.hospital import Hospital


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


def test_create_schedule_preference(db: Session, test_patient):
    """Test creating schedule preference."""
    preference = SchedulePreference(
        patient_id=test_patient.id,
        preferred_time=time(9, 0),  # 9 AM
        preferred_days=["monday", "wednesday", "friday"],
        channel_preference="ivr",
        frequency="weekly",
        timezone="Africa/Accra"
    )
    db.add(preference)
    db.commit()
    
    assert preference.patient_id == test_patient.id
    assert preference.preferred_time.hour == 9
    # TODO: Assert preference is properly linked


def test_schedule_preference_validation(db: Session, test_patient):
    """Test schedule preference validation."""
    # Test invalid time
    # TODO: Implement validation logic
    
    # Test invalid frequency
    # TODO: Implement validation logic
    
    pass


def test_get_patient_schedule_preference(db: Session, test_patient):
    """Test getting patient's schedule preference."""
    preference = SchedulePreference(
        patient_id=test_patient.id,
        preferred_time=time(10, 0),
        channel_preference="sms"
    )
    db.add(preference)
    db.commit()
    
    # Query preference
    found_preference = db.query(SchedulePreference).filter(
        SchedulePreference.patient_id == test_patient.id
    ).first()
    
    assert found_preference is not None
    assert found_preference.channel_preference == "sms"

