"""
Section ORM Model
=================

Represents a railway track section (e.g. between two stations/junctions).
"""

from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Section(Base):
    """Railway Track Section model."""

    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_station: Mapped[str] = mapped_column(String(50), nullable=False)
    end_station: Mapped[str] = mapped_column(String(50), nullable=False)
    length_km: Mapped[float] = mapped_column(Float, nullable=False)
    tracks_count: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    tasks: Mapped[list["MaintenanceTask"]] = relationship(
        "MaintenanceTask", back_populates="section", cascade="all, delete-orphan"
    )
    trains: Mapped[list["TrainSchedule"]] = relationship(
        "TrainSchedule", back_populates="section", cascade="all, delete-orphan"
    )
