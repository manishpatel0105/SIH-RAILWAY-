"""
Maintenance Task Pydantic Schemas
=================================
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator


class TaskUrgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    EMERGENCY = "EMERGENCY"


class TaskCriticality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"


class MaintenanceTaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(default=None)
    section_id: int = Field(..., gt=0, description="Foreign key reference to sections.id")
    department: str = Field(..., min_length=2, max_length=50, description="e.g. TRACK, SIGNAL, OHE, ELECTRICAL")
    duration_minutes: int = Field(..., gt=0, description="Duration in minutes (must be positive)")
    urgency: TaskUrgency = Field(default=TaskUrgency.MEDIUM)
    criticality: TaskCriticality = Field(default=TaskCriticality.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    requested_start_time: datetime | None = None
    requested_end_time: datetime | None = None

    @model_validator(mode="after")
    def validate_time_range(self) -> "MaintenanceTaskBase":
        if self.requested_start_time and self.requested_end_time:
            if self.requested_start_time >= self.requested_end_time:
                raise ValueError("requested_start_time must be strictly earlier than requested_end_time")
        return self


class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass


class MaintenanceTaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    section_id: int | None = Field(default=None, gt=0)
    department: str | None = Field(default=None, min_length=2, max_length=50)
    duration_minutes: int | None = Field(default=None, gt=0)
    urgency: TaskUrgency | None = None
    criticality: TaskCriticality | None = None
    status: TaskStatus | None = None
    requested_start_time: datetime | None = None
    requested_end_time: datetime | None = None

    @model_validator(mode="after")
    def validate_time_range(self) -> "MaintenanceTaskUpdate":
        if self.requested_start_time and self.requested_end_time:
            if self.requested_start_time >= self.requested_end_time:
                raise ValueError("requested_start_time must be strictly earlier than requested_end_time")
        return self


class MaintenanceTaskResponse(MaintenanceTaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskFilterParams(BaseModel):
    section_id: int | None = None
    department: str | None = None
    status: TaskStatus | None = None
