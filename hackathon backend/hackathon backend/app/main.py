"""
FastAPI Application Entrypoint
===============================

Creates and configures the main FastAPI application instance.
"""

import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.exceptions import AppException
from app.core.logging import setup_logging
from app.api.router import api_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown events."""
    settings = get_settings()
    logger.info(
        "Starting %s v%s (env=%s, debug=%s)",
        settings.app_name,
        settings.app_version,
        settings.app_env,
        settings.debug,
    )
    yield
    logger.info("Application shutdown complete.")


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    settings = get_settings()

    setup_logging(debug=settings.debug)

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "AI-Powered Automatic Block Planning to Maximize Asset Availability "
            "for Train Operations on Indian Railways."
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler for custom AppException domain errors
    @application.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                }
            },
        )

    # Register root endpoint
    @application.get("/", tags=["Root"])
    async def root():
        return {"message": "Railway Block Planning API is running"}

    # Register API routes (/api/v1/...)
    application.include_router(api_router)

    logger.info("Application initialized successfully.")
    return application


app = create_app()
