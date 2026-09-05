"""
Maintenance Tasks API Endpoints
===============================
"""

from collections.abc import Sequence
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.section_repository import SectionRepository
from app.repositories.task_repository import TaskRepository
from app.schemas.task import (
    MaintenanceTaskCreate,
    MaintenanceTaskResponse,
    MaintenanceTaskUpdate,
    TaskFilterParams,
    TaskStatus,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Maintenance Tasks"])


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    task_repo = TaskRepository(db)
    section_repo = SectionRepository(db)
    return TaskService(task_repo, section_repo)


@router.post("", response_model=MaintenanceTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: MaintenanceTaskCreate,
    service: TaskService = Depends(get_task_service),
) -> MaintenanceTaskResponse:
    """Create a new maintenance task block request."""
    return await service.create_task(data)


@router.get("", response_model=list[MaintenanceTaskResponse], status_code=status.HTTP_200_OK)
async def list_tasks(
    section_id: int | None = None,
    department: str | None = None,
    status_filter: TaskStatus | None = None,
    skip: int = 0,
    limit: int = 100,
    service: TaskService = Depends(get_task_service),
) -> Sequence[MaintenanceTaskResponse]:
    """List maintenance tasks with optional filtering by section_id, department, and status."""
    filters = TaskFilterParams(section_id=section_id, department=department, status=status_filter)
    return await service.list_tasks(filters=filters, skip=skip, limit=limit)


@router.get("/{id}", response_model=MaintenanceTaskResponse, status_code=status.HTTP_200_OK)
async def get_task(
    id: int,
    service: TaskService = Depends(get_task_service),
) -> MaintenanceTaskResponse:
    """Get a maintenance task by ID."""
    return await service.get_task(id)


@router.put("/{id}", response_model=MaintenanceTaskResponse, status_code=status.HTTP_200_OK)
async def update_task(
    id: int,
    data: MaintenanceTaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> MaintenanceTaskResponse:
    """Update an existing maintenance task by ID."""
    return await service.update_task(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete a maintenance task by ID."""
    await service.delete_task(id)
