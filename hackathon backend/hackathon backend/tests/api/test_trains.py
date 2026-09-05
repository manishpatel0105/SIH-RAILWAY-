"""
Tests for Train Schedules API
=============================
"""

from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


async def _create_test_section(client: AsyncClient, code: str = "SEC-TRAIN") -> int:
    payload = {
        "code": code,
        "name": "Test Section for Trains",
        "start_station": "NDLS",
        "end_station": "CNB",
        "length_km": 440.0,
    }
    res = await client.post("/api/v1/sections", json=payload)
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_train_success(client: AsyncClient):
    """Test successful train schedule creation."""
    sec_id = await _create_test_section(client, "SEC-TR1")
    train_payload = {
        "train_number": "12951",
        "train_name": "Rajdhani Express",
        "train_type": "EXPRESS",
        "section_id": sec_id,
        "departure_time": "2026-09-06T10:00:00Z",
        "arrival_time": "2026-09-06T14:30:00Z",
    }
    res = await client.post("/api/v1/trains", json=train_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["train_number"] == "12951"
    assert data["section_id"] == sec_id


@pytest.mark.asyncio
async def test_create_train_invalid_section_fk(client: AsyncClient):
    """Test creating train schedule with non-existent section returns 404."""
    train_payload = {
        "train_number": "12002",
        "train_name": "Shatabdi Express",
        "train_type": "SUPERFAST",
        "section_id": 999999,
        "departure_time": "2026-09-06T06:00:00Z",
        "arrival_time": "2026-09-06T09:00:00Z",
    }
    res = await client.post("/api/v1/trains", json=train_payload)
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_create_train_invalid_times(client: AsyncClient):
    """Test departure_time >= arrival_time fails schema validation (422)."""
    sec_id = await _create_test_section(client, "SEC-TR2")
    train_payload = {
        "train_number": "12004",
        "train_name": "Reverse Time Express",
        "train_type": "EXPRESS",
        "section_id": sec_id,
        "departure_time": "2026-09-06T14:00:00Z",
        "arrival_time": "2026-09-06T10:00:00Z",  # Earlier than departure!
    }
    res = await client.post("/api/v1/trains", json=train_payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_list_trains_with_filtering(client: AsyncClient):
    """Test filtering train schedules by section_id, train_date, and train_type."""
    sec1 = await _create_test_section(client, "SEC-TRF1")
    sec2 = await _create_test_section(client, "SEC-TRF2")

    # Train 1
    await client.post(
        "/api/v1/trains",
        json={
            "train_number": "T101",
            "train_name": "Freight 1",
            "train_type": "FREIGHT",
            "section_id": sec1,
            "departure_time": "2026-09-06T08:00:00Z",
            "arrival_time": "2026-09-06T12:00:00Z",
        },
    )
    # Train 2
    await client.post(
        "/api/v1/trains",
        json={
            "train_number": "T102",
            "train_name": "Express 1",
            "train_type": "EXPRESS",
            "section_id": sec1,
            "departure_time": "2026-09-06T13:00:00Z",
            "arrival_time": "2026-09-06T17:00:00Z",
        },
    )

    # Filter by section_id=sec1 & train_type=FREIGHT
    res = await client.get(f"/api/v1/trains?section_id={sec1}&train_type=FREIGHT")
    assert res.status_code == 200
    trains = res.json()
    assert len(trains) == 1
    assert trains[0]["train_number"] == "T101"

    # Filter by train_date
    res2 = await client.get("/api/v1/trains?train_date=2026-09-06")
    assert res2.status_code == 200
    assert len(res2.json()) == 2


@pytest.mark.asyncio
async def test_update_and_delete_train(client: AsyncClient):
    """Test updating and deleting a train schedule."""
    sec_id = await _create_test_section(client, "SEC-TRUD")
    create_res = await client.post(
        "/api/v1/trains",
        json={
            "train_number": "T999",
            "train_name": "Old Train",
            "train_type": "PASSENGER",
            "section_id": sec_id,
            "departure_time": "2026-09-06T08:00:00Z",
            "arrival_time": "2026-09-06T10:00:00Z",
        },
    )
    train_id = create_res.json()["id"]

    # Update
    upd_res = await client.put(f"/api/v1/trains/{train_id}", json={"train_name": "Updated Train"})
    assert upd_res.status_code == 200
    assert upd_res.json()["train_name"] == "Updated Train"

    # Delete
    del_res = await client.delete(f"/api/v1/trains/{train_id}")
    assert del_res.status_code == 204

    # Verify 404
    get_res = await client.get(f"/api/v1/trains/{train_id}")
    assert get_res.status_code == 404
