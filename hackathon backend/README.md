# Railway Block Planner

AI-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways.

> ⚠️ **Disclaimer**: This is a decision-support and optimization prototype using synthetic data. It does **not** directly control trains or railway signalling systems, and synthetic results do not represent actual Indian Railways performance.

## Quick Start

```bash
# Copy environment variables
cp .env.example .env

# Start with Docker (includes PostgreSQL database)
docker compose up --build

# Or run locally
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Database Setup & Administration

### 1. PostgreSQL Installation

#### Option A: Docker (Recommended)
PostgreSQL is included in `docker-compose.yml`:
```bash
docker compose up db -d
```

#### Option B: macOS (Homebrew)
```bash
brew install postgresql@16
brew services start postgresql@16
```

#### Option C: Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. Database Creation
Connect to your local PostgreSQL server and create the application database and user:
```sql
CREATE USER railway WITH PASSWORD 'railway_secret';
CREATE DATABASE railway_block_planner OWNER railway;
GRANT ALL PRIVILEGES ON DATABASE railway_block_planner TO railway;
```

### 3. Environment Configuration
Set the `DATABASE_URL` in your `.env` file:
```env
# Format: postgresql+asyncpg://<user>:<password>@<host>:<port>/<dbname>
DATABASE_URL=postgresql+asyncpg://railway:railway_secret@localhost:5432/railway_block_planner
```

### 4. Alembic Migration Commands
Apply database migrations or generate new schema updates:

```bash
# Apply all pending migrations to the database
alembic upgrade head

# Roll back the last migration
alembic downgrade -1

# Generate a new migration script after modifying models
alembic revision --autogenerate -m "describe_your_changes"

# View current migration version
alembic current
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
