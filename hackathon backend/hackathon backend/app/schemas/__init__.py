"""
Schemas Package
===============
Central registration of Pydantic schemas.
"""

from app.schemas.section import SectionCreate, SectionResponse, SectionUpdate
from app.schemas.task import (
    MaintenanceTaskCreate,
    MaintenanceTaskResponse,
    MaintenanceTaskUpdate,
    TaskFilterParams,
)
from app.schemas.train import (
    TrainFilterParams,
    TrainScheduleCreate,
    TrainScheduleResponse,
    TrainScheduleUpdate,
)

__all__ = [
    "SectionCreate",
    "SectionUpdate",
    "SectionResponse",
    "MaintenanceTaskCreate",
    "MaintenanceTaskUpdate",
    "MaintenanceTaskResponse",
    "TaskFilterParams",
    "TrainScheduleCreate",
    "TrainScheduleUpdate",
    "TrainScheduleResponse",
    "TrainFilterParams",
]
