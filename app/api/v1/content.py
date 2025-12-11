"""Content API endpoints (lessons, conditions, versions)."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/lessons")
async def list_lessons():
    """List all lessons."""
    pass


@router.get("/lessons/{lesson_id}")
async def get_lesson(lesson_id: int):
    """Get lesson by ID."""
    pass


@router.get("/conditions")
async def list_conditions():
    """List all conditions."""
    pass


@router.get("/conditions/{condition_id}")
async def get_condition(condition_id: int):
    """Get condition by ID."""
    pass


@router.get("/versions")
async def list_versions():
    """List all content versions."""
    pass

