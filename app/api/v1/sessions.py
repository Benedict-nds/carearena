"""Conversation sessions API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/")
async def list_sessions():
    """List all conversation sessions."""
    pass


@router.get("/{session_id}")
async def get_session(session_id: int):
    """Get session by ID."""
    pass


@router.post("/")
async def create_session():
    """Create a new conversation session."""
    pass


@router.get("/patient/{patient_id}")
async def get_patient_sessions(patient_id: int):
    """Get all sessions for a patient."""
    pass

