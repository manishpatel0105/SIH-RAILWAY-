"""
Section ORM Model
=================

Represents a track section in the railway network.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.maintenance_task import MaintenanceTask
    from app.models.train_schedule import TrainSchedule


class Section(Base):
    """
    Railway Track Section Model.

    A section is a specific portion of railway line identified by `section_code`
    (e.g., 'NDLS-CNB-01') between `km_start` and `km_end`.
    """

    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    section_code: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    route_from: Mapped[str] = mapped_column(String(100), nullable=False)
    route_to: Mapped[str] = mapped_column(String(100), nullable=False)
    km_start: Mapped[float] = mapped_column(Float, nullable=False)
    km_end: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="ACTIVE", server_default="ACTIVE"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships (1 -> Many)
    maintenance_tasks: Mapped[List["MaintenanceTask"]] = relationship(
        "MaintenanceTask",
        back_populates="section",
        cascade="all, delete-orphan",
    )
    train_schedules: Mapped[List["TrainSchedule"]] = relationship(
        "TrainSchedule",
        back_populates="section",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Section id={self.id} code='{self.section_code}' name='{self.name}'>"
