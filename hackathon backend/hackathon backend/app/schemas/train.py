"""
Train Schedule Pydantic Schemas
==============================
"""

from datetime import date as date_type, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator


class TrainType(str, Enum):
    EXPRESS = "EXPRESS"
    PASSENGER = "PASSENGER"
    FREIGHT = "FREIGHT"
    SUPERFAST = "SUPERFAST"


class TrainScheduleBase(BaseModel):
    train_number: str = Field(..., min_length=1, max_length=20)
    train_name: str = Field(..., min_length=2, max_length=100)
    train_type: TrainType = Field(default=TrainType.EXPRESS)
    section_id: int = Field(..., gt=0, description="Foreign key reference to sections.id")
    departure_time: datetime
    arrival_time: datetime

    @model_validator(mode="after")
    def validate_departure_arrival(self) -> "TrainScheduleBase":
        if self.departure_time >= self.arrival_time:
            raise ValueError("departure_time must be strictly earlier than arrival_time")
        return self


class TrainScheduleCreate(TrainScheduleBase):
    pass


class TrainScheduleUpdate(BaseModel):
    train_number: str | None = Field(default=None, min_length=1, max_length=20)
    train_name: str | None = Field(default=None, min_length=2, max_length=100)
    train_type: TrainType | None = None
    section_id: int | None = Field(default=None, gt=0)
    departure_time: datetime | None = None
    arrival_time: datetime | None = None

    @model_validator(mode="after")
    def validate_departure_arrival(self) -> "TrainScheduleUpdate":
        if self.departure_time and self.arrival_time:
            if self.departure_time >= self.arrival_time:
                raise ValueError("departure_time must be strictly earlier than arrival_time")
        return self


class TrainScheduleResponse(TrainScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainFilterParams(BaseModel):
    section_id: int | None = None
    date: date_type | None = None
    train_type: TrainType | None = None
