"""
FastAPI Application Entrypoint
===============================

This module creates and configures the FastAPI application instance.

WHAT HAPPENS AT STARTUP:
  1. Logging is configured (structured format, appropriate levels).
  2. The FastAPI app is created with metadata (title, version, description).
  3. CORS middleware is added so the frontend can talk to us.
  4. The v1 API router is registered under /api/v1.
  5. Lifespan events handle database engine startup/shutdown.

APPLICATION FACTORY PATTERN:
  We use `create_app()` to build the FastAPI instance. This lets us:
  - Create different app instances for testing (with mock DB, etc.)
  - Keep configuration separate from app creation
  - Follow the same pattern used by Flask and other frameworks

DISCLAIMER:
  This system is a decision-support and optimization prototype.
  It does NOT directly control trains or railway signalling.
  Synthetic data is used for demonstration purposes.
"""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import engine
from app.logging_config import setup_logging
from app.api.v1.router import v1_router

logger = logging.getLogger(__name__)


# ── Lifespan ──────────────────────────────────────────────────
# The lifespan context manager runs code at startup and shutdown.
# This replaces the deprecated @app.on_event("startup") pattern.


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage application startup and shutdown.

    Startup:
      - Log that the app is ready
    Shutdown:
      - Dispose the database engine (close all connections cleanly)
    """
    settings = get_settings()
    logger.info(
        "Starting %s v%s (debug=%s)",
        settings.app_name,
        settings.app_version,
        settings.debug,
    )
    yield
    # ── Shutdown ──────────────────────────────────────────
    logger.info("Shutting down — disposing database engine...")
    await engine.dispose()
    logger.info("Shutdown complete.")


# ── Application Factory ──────────────────────────────────────


def create_app() -> FastAPI:
    """
    Build and configure the FastAPI application.

    Returns:
        A fully configured FastAPI instance.
    """
    settings = get_settings()

    # 1. Configure logging first so everything else is logged properly
    setup_logging(debug=settings.debug)

    # 2. Create the FastAPI instance
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "AI-Powered Automatic Block Planning to Maximize Asset Availability "
            "for Train Operations on Indian Railways.\n\n"
            "⚠️ This is a decision-support prototype using synthetic data. "
            "It does not directly control railway operations."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 3. Add CORS middleware so the frontend can communicate with us
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4. Register API routers
    application.include_router(v1_router)

    logger.info("Application created successfully.")
    return application


# ── Module-level app instance ─────────────────────────────────
# Uvicorn expects `app.main:app` — this is the object it runs.
app = create_app()
