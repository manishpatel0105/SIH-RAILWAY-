"""
Repositories Package
=====================
Central registration of repository classes.
"""

from app.repositories.section_repository import SectionRepository
from app.repositories.task_repository import TaskRepository
from app.repositories.train_repository import TrainRepository

__all__ = ["SectionRepository", "TaskRepository", "TrainRepository"]
