"""
Main API Router
===============

Aggregates API routers across versions (e.g. v1, v2).
Mounted at /api in main application.
"""

from fastapi import APIRouter

from app.api.v1.router import v1_router

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
