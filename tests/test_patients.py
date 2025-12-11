"""Tests for patient CRUD operations."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.models.patient import Patient
from app.db.models.hospital import Hospital
from app.schemas.patient import PatientCreate

client = TestClient(app)


@pytest.fixture
def test_hospital(db: Session):
    """Create test hospital."""
    hospital = Hospital(name="Test Hospital", code="TEST001")
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


def test_create_patient(db: Session, test_hospital):
    """Test creating a patient."""
    patient_data = PatientCreate(
        hospital_id=test_hospital.id,
        first_name="John",
        last_name="Doe",
        phone_number="+233241234567",
        language_preference="en"
    )
    
    response = client.post("/api/v1/patients/", json=patient_data.dict())
    assert response.status_code == 200 or response.status_code == 201
    # TODO: Assert response data


def test_get_patient(db: Session, test_hospital):
    """Test getting a patient."""
    # Create patient first
    patient = Patient(
        hospital_id=test_hospital.id,
        first_name="Jane",
        last_name="Smith",
        phone_number="+233241234568"
    )
    db.add(patient)
    db.commit()
    
    response = client.get(f"/api/v1/patients/{patient.id}")
    assert response.status_code == 200
    # TODO: Assert response data


def test_list_patients(db: Session, test_hospital):
    """Test listing patients."""
    response = client.get("/api/v1/patients/")
    assert response.status_code == 200
    # TODO: Assert response data


def test_update_patient(db: Session, test_hospital):
    """Test updating a patient."""
    # TODO: Implement test
    pass


def test_delete_patient(db: Session, test_hospital):
    """Test deleting a patient."""
    # TODO: Implement test
    pass

