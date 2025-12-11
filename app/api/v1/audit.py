"""Audit log API endpoints."""

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/")
async def list_audit_logs():
    """List audit logs."""
    pass


@router.get("/{audit_id}")
async def get_audit_log(audit_id: int):
    """Get audit log by ID."""
    pass

