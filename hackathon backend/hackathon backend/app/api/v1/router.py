"""
API v1 Router
==============

Aggregates all v1 endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.sections import router as sections_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.trains import router as trains_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(health_router)
v1_router.include_router(sections_router)
v1_router.include_router(tasks_router)
v1_router.include_router(trains_router)
