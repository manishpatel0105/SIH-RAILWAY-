"""
Tests for Root and Health Endpoints
=====================================
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test that GET / returns expected welcome message."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Railway Block Planning API is running"}


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    """Test that GET /api/v1/health returns healthy status."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
