"""
Train Schedules API Endpoints
=============================
"""

from collections.abc import Sequence
from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.section_repository import SectionRepository
from app.repositories.train_repository import TrainRepository
from app.schemas.train import (
    TrainFilterParams,
    TrainScheduleCreate,
    TrainScheduleResponse,
    TrainScheduleUpdate,
    TrainType,
)
from app.services.train_service import TrainService

router = APIRouter(prefix="/trains", tags=["Train Schedules"])


def get_train_service(db: AsyncSession = Depends(get_db)) -> TrainService:
    train_repo = TrainRepository(db)
    section_repo = SectionRepository(db)
    return TrainService(train_repo, section_repo)


@router.post("", response_model=TrainScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_train(
    data: TrainScheduleCreate,
    service: TrainService = Depends(get_train_service),
) -> TrainScheduleResponse:
    """Create a new train schedule entry."""
    return await service.create_train(data)


@router.get("", response_model=list[TrainScheduleResponse], status_code=status.HTTP_200_OK)
async def list_trains(
    section_id: int | None = None,
    train_date: date | None = None,
    train_type: TrainType | None = None,
    skip: int = 0,
    limit: int = 100,
    service: TrainService = Depends(get_train_service),
) -> Sequence[TrainScheduleResponse]:
    """List train schedules with optional filtering by section_id, date, and train_type."""
    filters = TrainFilterParams(section_id=section_id, date=train_date, train_type=train_type)
    return await service.list_trains(filters=filters, skip=skip, limit=limit)


@router.get("/{id}", response_model=TrainScheduleResponse, status_code=status.HTTP_200_OK)
async def get_train(
    id: int,
    service: TrainService = Depends(get_train_service),
) -> TrainScheduleResponse:
    """Get a train schedule by ID."""
    return await service.get_train(id)


@router.put("/{id}", response_model=TrainScheduleResponse, status_code=status.HTTP_200_OK)
async def update_train(
    id: int,
    data: TrainScheduleUpdate,
    service: TrainService = Depends(get_train_service),
) -> TrainScheduleResponse:
    """Update an existing train schedule by ID."""
    return await service.update_train(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_train(
    id: int,
    service: TrainService = Depends(get_train_service),
) -> None:
    """Delete a train schedule by ID."""
    await service.delete_train(id)
