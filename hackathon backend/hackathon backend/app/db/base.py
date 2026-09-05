"""
SQLAlchemy Declarative Base
============================

This module defines the single `Base` class that ALL ORM models
in the project will inherit from.

WHY a single Base?
  - Alembic needs one `Base.metadata` to auto-detect all tables.
  - If models inherited from different bases, Alembic would miss some tables.
  - Having one base ensures consistency (e.g., shared naming conventions).

USAGE (in future phases):
    from app.db.base import Base

    class Section(Base):
        __tablename__ = "sections"
        id = mapped_column(Integer, primary_key=True)
        name = mapped_column(String(100), nullable=False)
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    All models inherit from this class. Alembic reads `Base.metadata`
    to generate migration scripts automatically.
    """

    pass
