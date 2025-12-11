"""Patient API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/")
async def list_patients():
    """List all patients."""
    pass


@router.get("/{patient_id}")
async def get_patient(patient_id: int):
    """Get patient by ID."""
    pass


@router.post("/")
async def create_patient():
    """Create a new patient."""
    pass


@router.put("/{patient_id}")
async def update_patient(patient_id: int):
    """Update patient."""
    pass


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int):
    """Delete patient."""
    pass

