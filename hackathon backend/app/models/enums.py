"""
Database Enums
==============

Enumeration types for Department, Safety, TaskStatus, and TrainType.
"""

from enum import Enum


class Department(str, Enum):
    """Railway maintenance departments."""

    ENGINEERING = "ENGINEERING"
    ELECTRICAL = "ELECTRICAL"
    SIGNAL = "SIGNAL"


class Safety(str, Enum):
    """Task safety impact levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    """Lifecycle status of a maintenance task."""

    PENDING = "PENDING"
    PRIORITIZED = "PRIORITIZED"
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TrainType(str, Enum):
    """Categorization of train operations."""

    EXPRESS = "EXPRESS"
    PASSENGER = "PASSENGER"
    GOODS = "GOODS"
    SPECIAL = "SPECIAL"
