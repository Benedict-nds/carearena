"""Scheduling API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/")
async def list_schedules():
    """List all scheduled calls."""
    pass


@router.get("/{schedule_id}")
async def get_schedule(schedule_id: int):
    """Get schedule by ID."""
    pass


@router.post("/")
async def create_schedule():
    """Create a new scheduled call."""
    pass


@router.put("/{schedule_id}")
async def update_schedule(schedule_id: int):
    """Update schedule."""
    pass


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: int):
    """Delete schedule."""
    pass

