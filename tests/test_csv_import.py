"""Tests for CSV import deduplication."""

import pytest
import csv
import tempfile
from sqlalchemy.orm import Session
from app.db.models.patient import Patient
from app.db.models.hospital import Hospital
from app.services.csv_importer import CSVImporterService


@pytest.fixture
def test_hospital(db: Session):
    """Create test hospital."""
    hospital = Hospital(name="Test Hospital", code="TEST001")
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital


def test_csv_import_deduplication(db: Session, test_hospital):
    """Test CSV import with duplicate phone numbers."""
    # Create existing patient
    existing_patient = Patient(
        hospital_id=test_hospital.id,
        first_name="Existing",
        last_name="Patient",
        phone_number="+233241234567"
    )
    db.add(existing_patient)
    db.commit()
    
    # Create CSV with duplicate phone number
    csv_data = [
        {"first_name": "New", "last_name": "Patient", "phone_number": "+233241234567"},
        {"first_name": "Another", "last_name": "Patient", "phone_number": "+233241234568"},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        writer = csv.DictWriter(f, fieldnames=["first_name", "last_name", "phone_number"])
        writer.writeheader()
        writer.writerows(csv_data)
        csv_path = f.name
    
    # Import CSV
    importer = CSVImporterService()
    result = importer.import_patients_from_csv(db, test_hospital.id, csv_path)
    
    # Should skip duplicate, import new one
    assert result["imported"] == 1
    assert result["skipped"] >= 1
    # TODO: Assert duplicate is not created


def test_csv_import_new_patients(db: Session, test_hospital):
    """Test CSV import with all new patients."""
    csv_data = [
        {"first_name": "John", "last_name": "Doe", "phone_number": "+233241234569"},
        {"first_name": "Jane", "last_name": "Smith", "phone_number": "+233241234570"},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        writer = csv.DictWriter(f, fieldnames=["first_name", "last_name", "phone_number"])
        writer.writeheader()
        writer.writerows(csv_data)
        csv_path = f.name
    
    importer = CSVImporterService()
    result = importer.import_patients_from_csv(db, test_hospital.id, csv_path)
    
    assert result["imported"] == 2
    assert result["errors"] == 0

