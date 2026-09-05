"""
Section Repository
==================

Database access layer for Section entities using SQLAlchemy AsyncSession.
"""

from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.section import Section
from app.schemas.section import SectionCreate, SectionUpdate


class SectionRepository:
    """Repository managing CRUD database operations for Section objects."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: SectionCreate) -> Section:
        """Create and persist a new Section record."""
        section = Section(**data.model_dump())
        self.db.add(section)
        await self.db.commit()
        await self.db.refresh(section)
        return section

    async def get_by_id(self, section_id: int) -> Section | None:
        """Fetch a Section by its primary key ID."""
        result = await self.db.execute(select(Section).where(Section.id == section_id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Section | None:
        """Fetch a Section by its unique code."""
        result = await self.db.execute(select(Section).where(Section.code == code))
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> Sequence[Section]:
        """Fetch all Sections with pagination."""
        result = await self.db.execute(select(Section).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, section: Section, data: SectionUpdate) -> Section:
        """Update an existing Section instance."""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(section, key, value)
        await self.db.commit()
        await self.db.refresh(section)
        return section

    async def delete(self, section: Section) -> None:
        """Delete a Section record."""
        await self.db.delete(section)
        await self.db.commit()
