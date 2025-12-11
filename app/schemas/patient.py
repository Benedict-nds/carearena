"""Patient schemas."""

from pydantic import BaseModel
from datetime import date
from typing import Optional


class PatientBase(BaseModel):
    """Base patient schema."""
    first_name: str
    last_name: str
    phone_number: str
    date_of_birth: Optional[date] = None
    language_preference: str = "en"


class PatientCreate(PatientBase):
    """Schema for creating a patient."""
    hospital_id: int


class PatientUpdate(BaseModel):
    """Schema for updating a patient."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    language_preference: Optional[str] = None
    is_active: Optional[bool] = None


class PatientResponse(PatientBase):
    """Schema for patient response."""
    id: int
    hospital_id: int
    is_active: bool
    
    class Config:
        from_attributes = True

