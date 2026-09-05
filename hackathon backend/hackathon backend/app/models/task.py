"""
Maintenance Task ORM Model
===========================

Represents a track/signal/OHE maintenance block request.
"""

from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MaintenanceTask(Base):
    """Maintenance Task model for track block requests."""

    __tablename__ = "maintenance_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    section_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sections.id", ondelete="CASCADE"), index=True, nullable=False
    )
    department: Mapped[str] = mapped_column(String(50), nullable=False)  # TRACK, SIGNAL, OHE, ELECTRICAL
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    urgency: Mapped[str] = mapped_column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, EMERGENCY
    criticality: Mapped[str] = mapped_column(String(20), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    status: Mapped[str] = mapped_column(String(20), default="PENDING", nullable=False)
    requested_start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
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
    section: Mapped["Section"] = relationship("Section", back_populates="tasks")
