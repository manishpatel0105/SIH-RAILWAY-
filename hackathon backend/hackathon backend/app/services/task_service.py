"""
Maintenance Task Service
========================

Business logic layer for MaintenanceTask management.
"""

from collections.abc import Sequence
from app.core.exceptions import NotFoundException, ValidationException
from app.models.task import MaintenanceTask
from app.repositories.section_repository import SectionRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import MaintenanceTaskCreate, MaintenanceTaskUpdate, TaskFilterParams


class TaskService:
    """Service orchestrating MaintenanceTask business rules and repository access."""

    def __init__(self, task_repo: TaskRepository, section_repo: SectionRepository):
        self.task_repo = task_repo
        self.section_repo = section_repo

    async def create_task(self, data: MaintenanceTaskCreate) -> MaintenanceTask:
        """Create a maintenance task ensuring valid section reference and duration."""
        # 1. Validate section FK existence
        section = await self.section_repo.get_by_id(data.section_id)
        if not section:
            raise NotFoundException(resource="Section", resource_id=data.section_id)

        # 2. Validate duration
        if data.duration_minutes <= 0:
            raise ValidationException("Duration must be a positive integer in minutes")

        # 3. Validate times if provided
        if data.requested_start_time and data.requested_end_time:
            if data.requested_start_time >= data.requested_end_time:
                raise ValidationException("requested_start_time must be strictly earlier than requested_end_time")

        return await self.task_repo.create(data)

    async def get_task(self, task_id: int) -> MaintenanceTask:
        """Fetch a maintenance task by ID or raise NotFoundException."""
        task = await self.task_repo.get_by_id(task_id)
        if not task:
            raise NotFoundException(resource="Task", resource_id=task_id)
        return task

    async def list_tasks(
        self, filters: TaskFilterParams, skip: int = 0, limit: int = 100
    ) -> Sequence[MaintenanceTask]:
        """Fetch tasks matching filters."""
        if filters.section_id is not None:
            section = await self.section_repo.get_by_id(filters.section_id)
            if not section:
                raise NotFoundException(resource="Section", resource_id=filters.section_id)
        return await self.task_repo.list_filtered(filters=filters, skip=skip, limit=limit)

    async def update_task(self, task_id: int, data: MaintenanceTaskUpdate) -> MaintenanceTask:
        """Update a maintenance task ensuring section FK and time range validity."""
        task = await self.get_task(task_id)

        if data.section_id is not None:
            section = await self.section_repo.get_by_id(data.section_id)
            if not section:
                raise NotFoundException(resource="Section", resource_id=data.section_id)

        if data.duration_minutes is not None and data.duration_minutes <= 0:
            raise ValidationException("Duration must be a positive integer in minutes")

        start_time = data.requested_start_time or task.requested_start_time
        end_time = data.requested_end_time or task.requested_end_time
        if start_time and end_time and start_time >= end_time:
            raise ValidationException("requested_start_time must be strictly earlier than requested_end_time")

        return await self.task_repo.update(task, data)

    async def delete_task(self, task_id: int) -> None:
        """Delete a task by ID or raise NotFoundException."""
        task = await self.get_task(task_id)
        await self.task_repo.delete(task)
