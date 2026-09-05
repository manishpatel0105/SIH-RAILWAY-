"""
Section Service
===============

Business logic layer for Section management.
"""

from collections.abc import Sequence
from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.models.section import Section
from app.repositories.section_repository import SectionRepository
from app.schemas.section import SectionCreate, SectionUpdate


class SectionService:
    """Service orchestrating Section business rules and repository access."""

    def __init__(self, repository: SectionRepository):
        self.repository = repository

    async def create_section(self, data: SectionCreate) -> Section:
        """Create a new section ensuring section code is unique."""
        existing = await self.repository.get_by_code(data.code)
        if existing:
            raise ConflictException(f"Section with code '{data.code}' already exists")
        return await self.repository.create(data)

    async def get_section(self, section_id: int) -> Section:
        """Get a section by ID or raise NotFoundException."""
        section = await self.repository.get_by_id(section_id)
        if not section:
            raise NotFoundException(resource="Section", resource_id=section_id)
        return section

    async def list_sections(self, skip: int = 0, limit: int = 100) -> Sequence[Section]:
        """List sections with pagination."""
        return await self.repository.list_all(skip=skip, limit=limit)

    async def update_section(self, section_id: int, data: SectionUpdate) -> Section:
        """Update a section or raise NotFoundException / ConflictException."""
        section = await self.get_section(section_id)
        if data.code and data.code != section.code:
            existing = await self.repository.get_by_code(data.code)
            if existing:
                raise ConflictException(f"Section with code '{data.code}' already exists")
        return await self.repository.update(section, data)

    async def delete_section(self, section_id: int) -> None:
        """Delete a section by ID or raise NotFoundException."""
        section = await self.get_section(section_id)
        await self.repository.delete(section)
