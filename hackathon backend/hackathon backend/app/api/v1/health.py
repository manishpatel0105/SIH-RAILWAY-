"""
Health Check Endpoint
======================

Provides a light-weight endpoint to verify that the application service is running.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verify application availability.",
)
async def health_check() -> HealthResponse:
    """Check if the application service is healthy."""
    return HealthResponse(status="healthy")
