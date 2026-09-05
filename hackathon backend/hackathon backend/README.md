# Railway Block Planner

AI-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways.

> ⚠️ **Disclaimer**: This is a decision-support and optimization prototype using synthetic data. It does **not** directly control trains or railway signalling systems, and synthetic results do not represent actual Indian Railways performance.

## Quick Start

```bash
# Copy environment variables
cp .env.example .env

# Start with Docker
docker compose up --build

# Or run locally
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architecture

```
API → Services → Repositories → Database
                 Services → Engines (Optimization)
```
