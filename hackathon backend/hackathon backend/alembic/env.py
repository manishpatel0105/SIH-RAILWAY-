"""
Alembic Migration Environment
===============================

This file is run by Alembic every time you create or apply a migration.
It connects Alembic to our SQLAlchemy models and database.

KEY POINTS:
  - We import `Base.metadata` so Alembic can auto-detect table changes.
  - We read `DATABASE_URL` from our app config (not hardcoded).
  - We replace the async driver (asyncpg) with the sync driver (psycopg2)
    because Alembic runs migrations synchronously.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import get_settings
from app.db.base import Base

# ── Alembic Config ────────────────────────────────────────────
config = context.config

# Set up Python logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic about our models' metadata
target_metadata = Base.metadata

# ── Get Database URL ──────────────────────────────────────────
# Alembic runs SYNCHRONOUSLY, so we need a sync database driver.
# Our app uses asyncpg (async), so we swap it for psycopg2 (sync).

settings = get_settings()
sync_database_url = settings.database_url.replace(
    "postgresql+asyncpg", "postgresql+psycopg2"
)
config.set_main_option("sqlalchemy.url", sync_database_url)


# ── Offline Migrations ───────────────────────────────────────
# "Offline" mode generates SQL scripts without connecting to the DB.
# Useful for reviewing migrations before applying them.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generates SQL, no DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ── Online Migrations ────────────────────────────────────────
# "Online" mode connects to the DB and applies migrations directly.

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connects to DB and applies changes)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ── Run ───────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
