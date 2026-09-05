# ──────────────────────────────────────────────────────────────
# Stage 1: Base image with dependencies
# ──────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

# Prevent Python from buffering stdout/stderr (important for Docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by asyncpg and ortools
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy only dependency definition first (Docker layer caching)
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir ".[dev]"

# ──────────────────────────────────────────────────────────────
# Stage 2: Application
# ──────────────────────────────────────────────────────────────
FROM base AS app

# Copy the rest of the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Default command: run the FastAPI dev server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
