"""Hospital schemas."""

from pydantic import BaseModel
from typing import Optional


class HospitalBase(BaseModel):
    """Base hospital schema."""
    name: str
    code: str
    address: Optional[str] = None
    phone_number: Optional[str] = None


class HospitalCreate(HospitalBase):
    """Schema for creating a hospital."""
    pass


class HospitalUpdate(BaseModel):
    """Schema for updating a hospital."""
    name: Optional[str] = None
    code: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None


class HospitalResponse(HospitalBase):
    """Schema for hospital response."""
    id: int
    
    class Config:
        from_attributes = True

