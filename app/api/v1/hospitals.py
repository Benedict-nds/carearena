"""Hospital API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


@router.get("/")
async def list_hospitals():
    """List all hospitals."""
    pass


@router.get("/{hospital_id}")
async def get_hospital(hospital_id: int):
    """Get hospital by ID."""
    pass


@router.post("/")
async def create_hospital():
    """Create a new hospital."""
    pass


@router.put("/{hospital_id}")
async def update_hospital(hospital_id: int):
    """Update hospital."""
    pass


@router.post("/{hospital_id}/import-csv")
async def import_hospital_csv(hospital_id: int):
    """Import patient data from CSV."""
    pass

