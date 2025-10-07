# QuantumTrade Stage 2 to Stage 3 Migration Guide

This guide helps you migrate your QuantumTrade installation from Stage 2 (local PostgreSQL) to Stage 3 (Supabase Cloud).

## Prerequisites

Before starting the migration, ensure you have:

1. Completed Stage 2 implementation
2. A Supabase Cloud account
3. Docker and Docker Compose installed
4. Python 3.11+ for running scripts

## Migration Steps

### Step 1: Create Supabase Cloud Project

1. Visit [https://supabase.com](https://supabase.com)
2. Sign up or log in to your account
3. Create a new project
4. Note the following information from your project settings:
    - **Database**: Host, Database name, User, Password, Port (5432)
    - **API**: Project URL, anon key, service_role key
    - **Auth**: JWT secret (under Auth → Settings)

### Step 2: Update Environment Configuration

1. Update your `.env` file with Supabase Cloud credentials:

```env
# Database Configuration (Supabase Cloud)
DATABASE_URL=postgresql://<USER>:<PASSWORD>@<HOST>:5432/<DB_NAME>

# Supabase API
SUPABASE_URL=https://<PROJECT_REF>.supabase.co
SUPABASE_ANON_KEY=<your_anon_key>
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>

# Optional (Auth)
SUPABASE_JWT_SECRET=<your_supabase_jwt_secret>

# Frontend Configuration
VITE_SUPABASE_URL=https://<PROJECT_REF>.supabase.co
VITE_SUPABASE_ANON_KEY=<your_anon_key>
```

### Step 3: Update Docker Configuration

Replace your `docker-compose.yml` with the simplified version:

```yaml
version: "3.9"

services:
    backend:
        build:
            context: ./backend
            dockerfile: Dockerfile
        container_name: quantumtrade_backend
        restart: always
        ports:
            - "8000:8000"
        env_file:
            - .env
        volumes:
            - ./backend:/app

    frontend:
        build:
            context: ./frontend
            dockerfile: Dockerfile
        container_name: quantumtrade_frontend
        restart: always
        depends_on:
            - backend
        ports:
            - "5173:5173"
        environment:
            - VITE_API_URL=http://localhost:8000
        volumes:
            - ./frontend:/app
```

### Step 4: Verify Configuration

Run the verification script to check your setup:

```bash
python scripts/verify_stage3.py
```

### Step 5: Initialize Database Tables

Start your services and initialize the database tables:

```bash
# Start services
docker-compose up -d

# Initialize tables
docker-compose exec backend python -c "
from src.database import models, connection
from src.database.init_supabase_tables import create_supabase_tables
models.Base.metadata.create_all(bind=connection.engine)
create_supabase_tables()
print('Tables created successfully')
"
```

### Step 6: Test the Migration

1. Visit the frontend: http://localhost:5173
2. Check the backend API: http://localhost:8000/docs
3. Verify database connection: http://localhost:8000/
4. Check Supabase Dashboard for tables

## Data Migration (Optional)

If you have existing data from Stage 2 that you want to migrate:

### Export Data from Local Database

```bash
# Export from your local PostgreSQL (Stage 2)
docker exec -t supabase-local pg_dump -U postgres postgres > quantumtrade_backup.sql
```

### Import Data to Supabase Cloud

```bash
# Import to Supabase Cloud
psql $DATABASE_URL < quantumtrade_backup.sql
```

## Troubleshooting

### Common Issues

#### Environment Variables Not Loading

-   Ensure `.env` file is in the project root
-   Check that variable names match exactly
-   Restart services after updating environment variables

#### Database Connection Failed

-   Verify DATABASE_URL format
-   Check Supabase project credentials
-   Ensure Supabase project is not paused

#### Services Not Starting

-   Check Docker logs: `docker-compose logs`
-   Verify Docker Compose syntax
-   Ensure all required files exist

### Verification Commands

```bash
# Check environment variables
docker-compose exec backend env

# Test database connection
docker-compose exec backend python -c "
import os
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute('SELECT 1')
    print('Database connection successful:', result.fetchone())
"

# Check Supabase client
docker-compose exec frontend npm list @supabase/supabase-js
```

## Rollback to Stage 2 (If Needed)

If you need to rollback to Stage 2:

1. Restore the previous `docker-compose.yml`:

```yaml
services:
    frontend:
        build:
            context: ./frontend
            dockerfile: Dockerfile
        ports:
            - "5173:5173"
        depends_on:
            - backend

    backend:
        build:
            context: ./backend
            dockerfile: Dockerfile
        ports:
            - "8000:8000"
        depends_on:
            - supabase-db
        environment:
            - DATABASE_URL=postgresql://postgres:postgres@supabase-db:5432/postgres
            - SUPABASE_URL=postgresql://postgres:postgres@supabase-db:5432/postgres
            - SUPABASE_KEY=local-dev-key

    supabase-db:
        container_name: supabase-local
        image: postgres:15
        restart: always
        volumes:
            - supabase_data:/var/lib/postgresql/data
            - ./backend/init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
        environment:
            - POSTGRES_DB=postgres
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=postgres
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U postgres"]
            interval: 10s
            timeout: 5s
            retries: 5

volumes:
    supabase_data:
```

2. Restore the previous `.env` configuration
3. Run `docker-compose up --build`

## Benefits of Stage 3

### Advantages Over Stage 2

-   **Managed Database**: No need to maintain local PostgreSQL
-   **Scalability**: Supabase Cloud scales automatically
-   **Built-in Features**: Auth, Storage, and Real-time capabilities
-   **Global CDN**: Faster access to your application
-   **Enterprise Security**: Production-grade security features
-   **Reduced Maintenance**: Less infrastructure to manage

### When to Stay on Stage 2

-   Development and testing only
-   No internet access requirements
-   Complete control over data
-   Cost sensitivity for small projects

## Next Steps

After successful migration:

1. Explore Supabase Dashboard features
2. Implement user authentication
3. Set up Row Level Security
4. Configure Storage buckets
5. Explore Edge Functions for serverless logic
6. Set up monitoring and alerts

This migration guide ensures a smooth transition from local development to cloud-ready deployment while maintaining all existing functionality.
