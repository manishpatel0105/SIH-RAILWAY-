"""
Tests for Sections API
======================
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_section(client: AsyncClient):
    """Test creating a new section."""
    payload = {
        "code": "NDLS-CNB-01",
        "name": "New Delhi - Kanpur Section 1",
        "start_station": "NDLS",
        "end_station": "CNB",
        "length_km": 440.5,
        "tracks_count": 2,
    }
    response = await client.post("/api/v1/sections", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "NDLS-CNB-01"
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_create_section_duplicate_code(client: AsyncClient):
    """Test duplicate code returns conflict error (409)."""
    payload = {
        "code": "NDLS-CNB-02",
        "name": "New Delhi - Kanpur Section 2",
        "start_station": "NDLS",
        "end_station": "CNB",
        "length_km": 440.5,
        "tracks_count": 2,
    }
    res1 = await client.post("/api/v1/sections", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/sections", json=payload)
    assert res2.status_code == 409
    assert res2.json()["error"]["code"] == "CONFLICT"


@pytest.mark.asyncio
async def test_get_section(client: AsyncClient):
    """Test fetching section by ID."""
    payload = {
        "code": "SEC-01",
        "name": "Section One",
        "start_station": "A",
        "end_station": "B",
        "length_km": 50.0,
    }
    create_res = await client.post("/api/v1/sections", json=payload)
    assert create_res.status_code == 201, f"Failed to create: {create_res.json()}"
    sec_id = create_res.json()["id"]

    get_res = await client.get(f"/api/v1/sections/{sec_id}")
    assert get_res.status_code == 200
    assert get_res.json()["code"] == "SEC-01"


@pytest.mark.asyncio
async def test_get_nonexistent_section(client: AsyncClient):
    """Test 404 for non-existent section."""
    response = await client.get("/api/v1/sections/999999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_update_section(client: AsyncClient):
    """Test updating section properties."""
    create_res = await client.post(
        "/api/v1/sections",
        json={
            "code": "SEC-UPDATE",
            "name": "Old Name",
            "start_station": "A",
            "end_station": "B",
            "length_km": 10.0,
        },
    )
    assert create_res.status_code == 201, f"Failed to create: {create_res.json()}"
    sec_id = create_res.json()["id"]

    update_res = await client.put(f"/api/v1/sections/{sec_id}", json={"name": "New Name", "length_km": 12.5})
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "New Name"
    assert update_res.json()["length_km"] == 12.5


@pytest.mark.asyncio
async def test_delete_section(client: AsyncClient):
    """Test deleting section."""
    create_res = await client.post(
        "/api/v1/sections",
        json={
            "code": "SEC-DEL",
            "name": "Delete Me",
            "start_station": "A",
            "end_station": "B",
            "length_km": 10.0,
        },
    )
    assert create_res.status_code == 201, f"Failed to create: {create_res.json()}"
    sec_id = create_res.json()["id"]

    del_res = await client.delete(f"/api/v1/sections/{sec_id}")
    assert del_res.status_code == 204

    get_res = await client.get(f"/api/v1/sections/{sec_id}")
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_section_negative_length_validation(client: AsyncClient):
    """Test schema validation rejects negative length_km."""
    payload = {
        "code": "SEC-NEG",
        "name": "Invalid Section",
        "start_station": "A",
        "end_station": "B",
        "length_km": -10.0,
    }
    response = await client.post("/api/v1/sections", json=payload)
    assert response.status_code == 422
