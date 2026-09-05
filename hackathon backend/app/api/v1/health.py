"""
Health Check Endpoint
======================

Provides a simple way to verify the application is running
and can connect to its dependencies (database, etc.).

WHY do we need this?
  - Docker health checks can call this endpoint
  - Load balancers use it to know if the server is ready
  - Developers use it as a quick "is it working?" test
  - It's the first endpoint we build, so it validates the entire stack
"""

import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


# ── Response Schema ───────────────────────────────────────────

class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str
    version: str
    database: str


# ── Endpoint ──────────────────────────────────────────────────

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verify application and database connectivity.",
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """
    Check if the application and database are healthy.

    Returns:
        HealthResponse with status, version, and database connectivity.
    """
    settings = get_settings()

    # Attempt a simple database query to verify connectivity
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        logger.error("Database health check failed: %s", exc)
        db_status = "unhealthy"

    overall_status = "healthy" if db_status == "healthy" else "degraded"

    return HealthResponse(
        status=overall_status,
        version=settings.app_version,
        database=db_status,
    )
