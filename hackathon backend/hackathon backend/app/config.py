"""
Centralized Application Configuration
======================================

All configuration is loaded from environment variables using Pydantic Settings.
This gives us:
  - Type safety     → values are validated at startup
  - Single source   → one place to find all config
  - .env support    → local dev uses a .env file
  - No hardcoding   → secrets never touch source code

HOW IT WORKS:
  1. Pydantic reads env vars (or .env file) at import time.
  2. If a required var is missing, the app fails fast with a clear error.
  3. Any module can import `get_settings()` to access configuration.
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Each field maps to an environment variable of the same name (case-insensitive).
    For example, the field `app_name` reads the env var `APP_NAME`.
    """

    # ── Application ──────────────────────────────────────────
    app_env: str = "development"
    app_name: str = "Railway Block Planner"
    app_version: str = "0.1.0"
    debug: bool = False

    # ── Database ─────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://railway:railway_secret@db:5432/railway_block_planner"

    # ── Redis ────────────────────────────────────────────────
    redis_url: str = "redis://redis:6379/0"

    # ── CORS ─────────────────────────────────────────────────
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Accept both JSON arrays and comma-separated strings from env vars."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        # Look for a .env file in the project root
        env_file=".env",
        # Environment variables are case-insensitive
        case_sensitive=False,
        # If an env var exists, it overrides the .env file
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    WHY lru_cache?
    We only need to read env vars once. Caching avoids re-parsing
    the .env file on every request. The cache lasts for the entire
    lifetime of the process.
    """
    return Settings()
