"""API v1 routers."""

from fastapi import APIRouter
from app.api.v1 import (
    patients,
    hospitals,
    content,
    sessions,
    schedule,
    audit,
    auth,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(patients.router)
api_router.include_router(hospitals.router)
api_router.include_router(content.router)
api_router.include_router(sessions.router)
api_router.include_router(schedule.router)
api_router.include_router(audit.router)
api_router.include_router(auth.router)
