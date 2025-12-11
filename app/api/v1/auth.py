"""Authentication API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    """Login endpoint."""
    pass


@router.post("/logout")
async def logout():
    """Logout endpoint."""
    pass


@router.post("/refresh")
async def refresh_token():
    """Refresh access token."""
    pass


@router.get("/me")
async def get_current_user():
    """Get current authenticated user."""
    pass

