"""
Database Models & Session Tests
================================

Tests for Section, MaintenanceTask, and TrainSchedule models, relationships,
enums, cascade deletions, and database session injection.
"""

from datetime import date, datetime, time, timezone

import pytest
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

from app.db.base import Base
from app.db.database import get_db
from app.models import (
    Department,
    MaintenanceTask,
    Safety,
    Section,
    TaskStatus,
    TrainSchedule,
    TrainType,
)


@pytest.fixture
async def in_memory_db():
    """Set up an in-memory SQLite database for testing."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


async def test_create_section(in_memory_db: AsyncSession):
    """Verify Section creation and retrieval."""
    section = Section(
        section_code="NDLS-CNB-01",
        name="New Delhi - Kanpur Central",
        route_from="New Delhi",
        route_to="Kanpur Central",
        km_start=0.0,
        km_end=440.5,
        status="ACTIVE",
    )
    in_memory_db.add(section)
    await in_memory_db.commit()
    await in_memory_db.refresh(section)

    assert section.id is not None
    assert section.section_code == "NDLS-CNB-01"
    assert repr(section) == "<Section id=1 code='NDLS-CNB-01' name='New Delhi - Kanpur Central'>"


async def test_section_relationships_and_cascades(in_memory_db: AsyncSession):
    """Verify 1-to-many relationships and cascade deletion."""
    section = Section(
        section_code="BCT-NDLS-02",
        name="Mumbai Central - New Delhi",
        route_from="Mumbai Central",
        route_to="New Delhi",
        km_start=0.0,
        km_end=1384.0,
    )
    in_memory_db.add(section)
    await in_memory_db.flush()

    # Add MaintenanceTask
    task = MaintenanceTask(
        section_id=section.id,
        department=Department.ENGINEERING,
        task_type="Track Tamping",
        description="Deep screening and track tamping",
        duration_minutes=240,
        criticality=4,
        urgency=5,
        overdue_days=3,
        safety_impact=Safety.HIGH,
        required_resources={"machines": ["CSM", "DGS"], "crew": 8},
        deadline=datetime.now(timezone.utc),
        status=TaskStatus.PENDING,
    )

    # Add TrainSchedule
    train = TrainSchedule(
        train_number="12951",
        train_name="Rajdhani Express",
        train_type=TrainType.EXPRESS,
        section_id=section.id,
        date=date(2026, 9, 10),
        arrival_time=time(16, 55),
        departure_time=time(17, 0),
        priority=1,
    )

    in_memory_db.add_all([task, train])
    await in_memory_db.commit()

    # Query section with eager loaded relationships
    stmt = (
        select(Section)
        .options(
            selectinload(Section.maintenance_tasks),
            selectinload(Section.train_schedules),
        )
        .where(Section.id == section.id)
    )
    result = await in_memory_db.execute(stmt)
    fetched_section = result.scalar_one()

    assert len(fetched_section.maintenance_tasks) == 1
    assert fetched_section.maintenance_tasks[0].task_type == "Track Tamping"
    assert fetched_section.maintenance_tasks[0].department == Department.ENGINEERING
    assert fetched_section.maintenance_tasks[0].status == TaskStatus.PENDING

    assert len(fetched_section.train_schedules) == 1
    assert fetched_section.train_schedules[0].train_number == "12951"
    assert fetched_section.train_schedules[0].train_type == TrainType.EXPRESS

    # Test cascade delete
    await in_memory_db.delete(fetched_section)
    await in_memory_db.commit()

    tasks_res = await in_memory_db.execute(select(MaintenanceTask))
    trains_res = await in_memory_db.execute(select(TrainSchedule))
    assert len(tasks_res.scalars().all()) == 0
    assert len(trains_res.scalars().all()) == 0


async def test_get_db_dependency():
    """Verify get_db session generator."""
    session_generator = get_db()
    session = await anext(session_generator)
    assert isinstance(session, AsyncSession)
    await session_generator.aclose()
