"""
Services Package
================
Central registration of business service classes.
"""

from app.services.section_service import SectionService
from app.services.task_service import TaskService
from app.services.train_service import TrainService

__all__ = ["SectionService", "TaskService", "TrainService"]
