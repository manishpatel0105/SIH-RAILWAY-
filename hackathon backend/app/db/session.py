"""
Database Session Management
============================

This module creates the SQLAlchemy async engine and session factory,
and exposes a dependency for FastAPI route handlers.

KEY CONCEPTS FOR BEGINNERS:
  - **Engine**: The connection to the database. Think of it as a "pipe"
    between Python and PostgreSQL.
  - **Session**: A single "conversation" with the database. Each API request
    gets its own session, so requests don't interfere with each other.
  - **Dependency Injection**: FastAPI's `Depends(get_db)` automatically
    creates a session at the start of a request and closes it at the end.
    You never have to manage this manually.

HOW IT WORKS:
  1. `create_async_engine()` opens a connection pool to PostgreSQL.
  2. `async_sessionmaker()` creates a factory that produces sessions.
  3. `get_db()` is an async generator that yields a session and ensures
     it is closed after the request finishes (even if an error occurs).
"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

logger = logging.getLogger(__name__)

# ── Engine ────────────────────────────────────────────────────
# The engine manages a pool of database connections.
# pool_pre_ping=True checks if a connection is alive before using it,
# which prevents "connection closed" errors after idle periods.

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,       # Log SQL statements when DEBUG=true
    pool_pre_ping=True,        # Verify connections before use
    pool_size=5,               # Number of persistent connections
    max_overflow=10,           # Extra connections allowed under load
)

# ── Session Factory ───────────────────────────────────────────
# This factory creates new AsyncSession instances on demand.
# expire_on_commit=False means we can still access attributes
# after committing, which is useful for returning data in API responses.

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── FastAPI Dependency ────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for a single request.

    Usage in a route handler:
        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...

    The session is automatically closed when the request ends.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
