"""
Section Pydantic Schemas
========================
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class SectionBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50, description="Unique section identifier (e.g. NDLS-CNB-01)")
    name: str = Field(..., min_length=1, max_length=100, description="Descriptive section name")
    start_station: str = Field(..., min_length=1, max_length=50)
    end_station: str = Field(..., min_length=1, max_length=50)
    length_km: float = Field(..., gt=0, description="Section length in kilometers")
    tracks_count: int = Field(default=2, gt=0, description="Number of tracks")


class SectionCreate(SectionBase):
    pass


class SectionUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    start_station: str | None = Field(default=None, min_length=1, max_length=50)
    end_station: str | None = Field(default=None, min_length=1, max_length=50)
    length_km: float | None = Field(default=None, gt=0)
    tracks_count: int | None = Field(default=None, gt=0)


class SectionResponse(SectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
