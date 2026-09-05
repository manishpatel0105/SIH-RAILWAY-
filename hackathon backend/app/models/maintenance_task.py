"""
MaintenanceTask ORM Model
=========================

Represents a requested maintenance work block on a section.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

from sqlalchemy import (
    JSON,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Department, Safety, TaskStatus

if TYPE_CHECKING:
    from app.models.section import Section


class MaintenanceTask(Base):
    """
    Maintenance Task Model.

    Tracks maintenance requirements, resources, criticality, safety impact,
    and current status for block scheduling on railway sections.
    """

    __tablename__ = "maintenance_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    department: Mapped[Department] = mapped_column(
        SQLEnum(Department, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        index=True,
    )
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    criticality: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    urgency: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    overdue_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    safety_impact: Mapped[Safety] = mapped_column(
        SQLEnum(Safety, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    required_resources: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, nullable=True
    )
    preferred_start_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    preferred_end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskStatus.PENDING,
        server_default=TaskStatus.PENDING.value,
        index=True,
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

    # Many -> 1 Relationship
    section: Mapped["Section"] = relationship("Section", back_populates="maintenance_tasks")

    def __repr__(self) -> str:
        return (
            f"<MaintenanceTask id={self.id} dept='{self.department.value}' "
            f"type='{self.task_type}' status='{self.status.value}'>"
        )
