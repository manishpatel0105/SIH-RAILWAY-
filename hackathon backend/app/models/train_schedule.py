"""
TrainSchedule ORM Model
=======================

Represents scheduled train runs through a section.
"""

from datetime import date, datetime, time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Date,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Time,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import TrainType

if TYPE_CHECKING:
    from app.models.section import Section


class TrainSchedule(Base):
    """
    Train Schedule Model.

    Tracks scheduled trains running through a section for collision check
    and availability window calculation.
    """

    __tablename__ = "train_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    train_number: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    train_name: Mapped[str] = mapped_column(String(100), nullable=False)
    train_type: Mapped[TrainType] = mapped_column(
        SQLEnum(TrainType, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    arrival_time: Mapped[time] = mapped_column(Time, nullable=False)
    departure_time: Mapped[time] = mapped_column(Time, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Many -> 1 Relationship
    section: Mapped["Section"] = relationship("Section", back_populates="train_schedules")

    def __repr__(self) -> str:
        return (
            f"<TrainSchedule id={self.id} train='{self.train_number}' "
            f"name='{self.train_name}' date='{self.date}'>"
        )
