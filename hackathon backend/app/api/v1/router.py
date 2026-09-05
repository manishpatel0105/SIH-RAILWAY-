"""
API v1 Router
==============

This module aggregates all v1 sub-routers into a single router.
The main application mounts this router under /api/v1.

WHY aggregate here?
  - Keeps main.py clean — it only knows about "v1 router", not every endpoint.
  - Adding new endpoint groups (sections, blocks, schedules) means
    just adding one `include_router()` line here.
  - If we ever create v2, we create a parallel app/api/v2/router.py.
"""

from fastapi import APIRouter

from app.api.v1.health import router as health_router

# Create the v1 router that groups all v1 endpoints
v1_router = APIRouter(prefix="/api/v1")

# ── Include sub-routers ──────────────────────────────────────
v1_router.include_router(health_router)
