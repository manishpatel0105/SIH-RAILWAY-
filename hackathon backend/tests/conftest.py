"""
Shared Test Fixtures
=====================

pytest "fixtures" are reusable pieces of test setup.
Any test file can use these fixtures by adding them as function parameters.

KEY FIXTURE — `client`:
  Creates a test HTTP client that talks to our FastAPI app
  WITHOUT starting a real server. This makes tests fast and isolated.

WHY httpx.AsyncClient?
  FastAPI recommends httpx for async testing. It simulates HTTP requests
  in-memory, so tests run in milliseconds instead of seconds.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """
    Provide an async HTTP test client.

    Usage in a test:
        async def test_something(client: AsyncClient):
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
