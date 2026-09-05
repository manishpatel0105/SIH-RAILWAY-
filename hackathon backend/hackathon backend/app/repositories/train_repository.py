"""
Train Schedule Repository
=========================

Database access layer for TrainSchedule entities.
"""

from collections.abc import Sequence
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.train import TrainSchedule
from app.schemas.train import TrainFilterParams, TrainScheduleCreate, TrainScheduleUpdate


class TrainRepository:
    """Repository managing CRUD database operations for TrainSchedule objects."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: TrainScheduleCreate) -> TrainSchedule:
        """Create and persist a new TrainSchedule record."""
        payload = data.model_dump()
        if isinstance(payload.get("train_type"), Enum):
            payload["train_type"] = payload["train_type"].value

        train = TrainSchedule(**payload)
        self.db.add(train)
        await self.db.commit()
        await self.db.refresh(train)
        return train

    async def get_by_id(self, train_id: int) -> TrainSchedule | None:
        """Fetch a TrainSchedule by primary key ID."""
        result = await self.db.execute(select(TrainSchedule).where(TrainSchedule.id == train_id))
        return result.scalar_one_or_none()

    async def list_filtered(
        self, filters: TrainFilterParams, skip: int = 0, limit: int = 100
    ) -> Sequence[TrainSchedule]:
        """Fetch TrainSchedules matching filtering parameters."""
        stmt = select(TrainSchedule)

        if filters.section_id is not None:
            stmt = stmt.where(TrainSchedule.section_id == filters.section_id)
        if filters.train_type is not None:
            train_type_val = (
                filters.train_type.value if hasattr(filters.train_type, "value") else filters.train_type
            )
            stmt = stmt.where(TrainSchedule.train_type == train_type_val)
        if filters.date is not None:
            start_dt = datetime.combine(filters.date, datetime.min.time()).replace(tzinfo=timezone.utc)
            end_dt = datetime.combine(filters.date, datetime.max.time()).replace(tzinfo=timezone.utc)
            stmt = stmt.where(TrainSchedule.departure_time >= start_dt, TrainSchedule.departure_time <= end_dt)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, train: TrainSchedule, data: TrainScheduleUpdate) -> TrainSchedule:
        """Update an existing TrainSchedule record."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(value, "value"):
                value = value.value
            setattr(train, key, value)
        await self.db.commit()
        await self.db.refresh(train)
        return train

    async def delete(self, train: TrainSchedule) -> None:
        """Delete a TrainSchedule record."""
        await self.db.delete(train)
        await self.db.commit()
