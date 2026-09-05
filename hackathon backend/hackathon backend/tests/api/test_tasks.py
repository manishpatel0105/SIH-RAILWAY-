"""
Tests for Maintenance Tasks API
================================
"""

import pytest
from httpx import AsyncClient


async def _create_test_section(client: AsyncClient, code: str = "SEC-TASK") -> int:
    payload = {
        "code": code,
        "name": "Test Section for Tasks",
        "start_station": "STA",
        "end_station": "STB",
        "length_km": 100.0,
    }
    res = await client.post("/api/v1/sections", json=payload)
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_task_success(client: AsyncClient):
    """Test successful task creation with valid section reference."""
    sec_id = await _create_test_section(client, "SEC-T1")
    task_payload = {
        "title": "OHE Line Inspection",
        "description": "Routine overhead line maintenance",
        "section_id": sec_id,
        "department": "OHE",
        "duration_minutes": 120,
        "urgency": "HIGH",
        "criticality": "MEDIUM",
        "status": "PENDING",
    }
    res = await client.post("/api/v1/tasks", json=task_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "OHE Line Inspection"
    assert data["section_id"] == sec_id


@pytest.mark.asyncio
async def test_create_task_invalid_section_fk(client: AsyncClient):
    """Test creating task with non-existent section_id returns 404."""
    task_payload = {
        "title": "Track Repair",
        "section_id": 999999,
        "department": "TRACK",
        "duration_minutes": 60,
        "urgency": "LOW",
        "criticality": "LOW",
    }
    res = await client.post("/api/v1/tasks", json=task_payload)
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_create_task_negative_duration(client: AsyncClient):
    """Test creating task with negative duration fails validation (422)."""
    sec_id = await _create_test_section(client, "SEC-T2")
    task_payload = {
        "title": "Invalid Duration Task",
        "section_id": sec_id,
        "department": "SIGNAL",
        "duration_minutes": -30,
        "urgency": "LOW",
        "criticality": "LOW",
    }
    res = await client.post("/api/v1/tasks", json=task_payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_task_invalid_urgency(client: AsyncClient):
    """Test creating task with invalid urgency enum fails (422)."""
    sec_id = await _create_test_section(client, "SEC-T3")
    task_payload = {
        "title": "Invalid Urgency Task",
        "section_id": sec_id,
        "department": "TRACK",
        "duration_minutes": 60,
        "urgency": "SUPER_URGENT",  # Invalid enum value
        "criticality": "HIGH",
    }
    res = await client.post("/api/v1/tasks", json=task_payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_list_tasks_with_filtering(client: AsyncClient):
    """Test filtering tasks by section_id, department, and status."""
    sec1 = await _create_test_section(client, "SEC-F1")
    sec2 = await _create_test_section(client, "SEC-F2")

    # Task 1
    await client.post(
        "/api/v1/tasks",
        json={
            "title": "T1",
            "section_id": sec1,
            "department": "TRACK",
            "duration_minutes": 60,
            "status": "PENDING",
        },
    )
    # Task 2
    await client.post(
        "/api/v1/tasks",
        json={
            "title": "T2",
            "section_id": sec1,
            "department": "OHE",
            "duration_minutes": 90,
            "status": "APPROVED",
        },
    )
    # Task 3
    await client.post(
        "/api/v1/tasks",
        json={
            "title": "T3",
            "section_id": sec2,
            "department": "TRACK",
            "duration_minutes": 120,
            "status": "PENDING",
        },
    )

    # Filter by department=TRACK
    res = await client.get("/api/v1/tasks?department=TRACK")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 2
    assert all(t["department"] == "TRACK" for t in tasks)

    # Filter by section_id=sec1 & status=APPROVED
    res2 = await client.get(f"/api/v1/tasks?section_id={sec1}&status_filter=APPROVED")
    assert res2.status_code == 200
    tasks2 = res2.json()
    assert len(tasks2) == 1
    assert tasks2[0]["title"] == "T2"


@pytest.mark.asyncio
async def test_update_and_delete_task(client: AsyncClient):
    """Test updating and deleting a task."""
    sec_id = await _create_test_section(client, "SEC-TUD")
    create_res = await client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "section_id": sec_id, "department": "TRACK", "duration_minutes": 60},
    )
    task_id = create_res.json()["id"]

    # Update
    upd_res = await client.put(f"/api/v1/tasks/{task_id}", json={"title": "Updated Title", "duration_minutes": 180})
    assert upd_res.status_code == 200
    assert upd_res.json()["title"] == "Updated Title"
    assert upd_res.json()["duration_minutes"] == 180

    # Delete
    del_res = await client.delete(f"/api/v1/tasks/{task_id}")
    assert del_res.status_code == 204

    # Verify 404
    get_res = await client.get(f"/api/v1/tasks/{task_id}")
    assert get_res.status_code == 404
