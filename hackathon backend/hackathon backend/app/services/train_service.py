"""
Train Schedule Service
======================

Business logic layer for TrainSchedule management.
"""

from collections.abc import Sequence
from app.core.exceptions import NotFoundException, ValidationException
from app.models.train import TrainSchedule
from app.repositories.section_repository import SectionRepository
from app.repositories.train_repository import TrainRepository
from app.schemas.train import TrainFilterParams, TrainScheduleCreate, TrainScheduleUpdate


class TrainService:
    """Service orchestrating TrainSchedule business rules and repository access."""

    def __init__(self, train_repo: TrainRepository, section_repo: SectionRepository):
        self.train_repo = train_repo
        self.section_repo = section_repo

    async def create_train(self, data: TrainScheduleCreate) -> TrainSchedule:
        """Create a train schedule ensuring section FK existence and valid times."""
        section = await self.section_repo.get_by_id(data.section_id)
        if not section:
            raise NotFoundException(resource="Section", resource_id=data.section_id)

        if data.departure_time >= data.arrival_time:
            raise ValidationException("departure_time must be strictly earlier than arrival_time")

        return await self.train_repo.create(data)

    async def get_train(self, train_id: int) -> TrainSchedule:
        """Fetch a train schedule by ID or raise NotFoundException."""
        train = await self.train_repo.get_by_id(train_id)
        if not train:
            raise NotFoundException(resource="TrainSchedule", resource_id=train_id)
        return train

    async def list_trains(
        self, filters: TrainFilterParams, skip: int = 0, limit: int = 100
    ) -> Sequence[TrainSchedule]:
        """Fetch train schedules matching filters."""
        if filters.section_id is not None:
            section = await self.section_repo.get_by_id(filters.section_id)
            if not section:
                raise NotFoundException(resource="Section", resource_id=filters.section_id)
        return await self.train_repo.list_filtered(filters=filters, skip=skip, limit=limit)

    async def update_train(self, train_id: int, data: TrainScheduleUpdate) -> TrainSchedule:
        """Update a train schedule ensuring section FK and time range validity."""
        train = await self.get_train(train_id)

        if data.section_id is not None:
            section = await self.section_repo.get_by_id(data.section_id)
            if not section:
                raise NotFoundException(resource="Section", resource_id=data.section_id)

        dep_time = data.departure_time or train.departure_time
        arr_time = data.arrival_time or train.arrival_time
        if dep_time >= arr_time:
            raise ValidationException("departure_time must be strictly earlier than arrival_time")

        return await self.train_repo.update(train, data)

    async def delete_train(self, train_id: int) -> None:
        """Delete a train schedule by ID or raise NotFoundException."""
        train = await self.get_train(train_id)
        await self.train_repo.delete(train)
