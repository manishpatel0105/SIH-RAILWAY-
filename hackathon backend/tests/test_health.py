"""
Health Endpoint Tests
======================

These tests verify that:
  1. The application starts correctly.
  2. The /api/v1/health endpoint is reachable.
  3. The response has the expected structure.

NOTE:
  These tests use the real database connection. If the database
  is unavailable, the health check should still respond (with
  database="unhealthy"). This is intentional — the health check
  should never crash, even when dependencies are down.
"""

from httpx import AsyncClient


async def test_health_returns_200(client: AsyncClient) -> None:
    """Health endpoint should return HTTP 200."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


async def test_health_response_structure(client: AsyncClient) -> None:
    """Health endpoint should return status, version, and database fields."""
    response = await client.get("/api/v1/health")
    data = response.json()

    assert "status" in data
    assert "version" in data
    assert "database" in data


async def test_health_version_matches_config(client: AsyncClient) -> None:
    """The version in the health response should match app config."""
    from app.config import get_settings

    response = await client.get("/api/v1/health")
    data = response.json()

    assert data["version"] == get_settings().app_version
