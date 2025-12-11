"""Patient service."""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    """Service for patient operations."""
    
    @staticmethod
    def get_patient(db: Session, patient_id: int) -> Optional[Patient]:
        """Get patient by ID."""
        return db.query(Patient).filter(Patient.id == patient_id).first()
    
    @staticmethod
    def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get all patients."""
        return db.query(Patient).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_patient(db: Session, patient_data: PatientCreate) -> Patient:
        """Create a new patient."""
        patient = Patient(**patient_data.dict())
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def update_patient(db: Session, patient_id: int, patient_data: PatientUpdate) -> Optional[Patient]:
        """Update a patient."""
        patient = PatientService.get_patient(db, patient_id)
        if not patient:
            return None
        
        update_data = patient_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(patient, field, value)
        
        db.commit()
        db.refresh(patient)
        return patient
    
    @staticmethod
    def delete_patient(db: Session, patient_id: int) -> bool:
        """Delete a patient."""
        patient = PatientService.get_patient(db, patient_id)
        if not patient:
            return False
        
        db.delete(patient)
        db.commit()
        return True

