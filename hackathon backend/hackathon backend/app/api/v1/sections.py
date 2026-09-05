"""
Section API Endpoints
=====================
"""

from collections.abc import Sequence
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.section_repository import SectionRepository
from app.schemas.section import SectionCreate, SectionResponse, SectionUpdate
from app.services.section_service import SectionService

router = APIRouter(prefix="/sections", tags=["Sections"])


def get_section_service(db: AsyncSession = Depends(get_db)) -> SectionService:
    repository = SectionRepository(db)
    return SectionService(repository)


@router.post("", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    data: SectionCreate,
    service: SectionService = Depends(get_section_service),
) -> SectionResponse:
    """Create a new railway track section."""
    return await service.create_section(data)


@router.get("", response_model=list[SectionResponse], status_code=status.HTTP_200_OK)
async def list_sections(
    skip: int = 0,
    limit: int = 100,
    service: SectionService = Depends(get_section_service),
) -> Sequence[SectionResponse]:
    """List all railway track sections with pagination."""
    return await service.list_sections(skip=skip, limit=limit)


@router.get("/{id}", response_model=SectionResponse, status_code=status.HTTP_200_OK)
async def get_section(
    id: int,
    service: SectionService = Depends(get_section_service),
) -> SectionResponse:
    """Get a section by ID."""
    return await service.get_section(id)


@router.put("/{id}", response_model=SectionResponse, status_code=status.HTTP_200_OK)
async def update_section(
    id: int,
    data: SectionUpdate,
    service: SectionService = Depends(get_section_service),
) -> SectionResponse:
    """Update an existing section by ID."""
    return await service.update_section(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    id: int,
    service: SectionService = Depends(get_section_service),
) -> None:
    """Delete a section by ID."""
    await service.delete_section(id)
