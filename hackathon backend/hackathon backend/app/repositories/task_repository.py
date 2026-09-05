"""
Maintenance Task Repository
===========================

Database access layer for MaintenanceTask entities.
"""

from collections.abc import Sequence
from enum import Enum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import MaintenanceTask
from app.schemas.task import MaintenanceTaskCreate, MaintenanceTaskUpdate, TaskFilterParams


class TaskRepository:
    """Repository managing CRUD database operations for MaintenanceTask objects."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: MaintenanceTaskCreate) -> MaintenanceTask:
        """Create and persist a new MaintenanceTask record."""
        payload = data.model_dump()
        if isinstance(payload.get("urgency"), Enum):
            payload["urgency"] = payload["urgency"].value
        if isinstance(payload.get("criticality"), Enum):
            payload["criticality"] = payload["criticality"].value
        if isinstance(payload.get("status"), Enum):
            payload["status"] = payload["status"].value

        task = MaintenanceTask(**payload)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_id(self, task_id: int) -> MaintenanceTask | None:
        """Fetch a MaintenanceTask by primary key ID."""
        result = await self.db.execute(select(MaintenanceTask).where(MaintenanceTask.id == task_id))
        return result.scalar_one_or_none()

    async def list_filtered(
        self, filters: TaskFilterParams, skip: int = 0, limit: int = 100
    ) -> Sequence[MaintenanceTask]:
        """Fetch MaintenanceTasks matching filtering parameters."""
        stmt = select(MaintenanceTask)

        if filters.section_id is not None:
            stmt = stmt.where(MaintenanceTask.section_id == filters.section_id)
        if filters.department is not None:
            stmt = stmt.where(MaintenanceTask.department == filters.department)
        if filters.status is not None:
            status_val = filters.status.value if hasattr(filters.status, "value") else filters.status
            stmt = stmt.where(MaintenanceTask.status == status_val)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, task: MaintenanceTask, data: MaintenanceTaskUpdate) -> MaintenanceTask:
        """Update an existing MaintenanceTask record."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(value, "value"):
                value = value.value
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: MaintenanceTask) -> None:
        """Delete a MaintenanceTask record."""
        await self.db.delete(task)
        await self.db.commit()
