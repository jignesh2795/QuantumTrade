@echo off
REM Script to sync data between Supabase and local Postgres mirror
REM Can be run manually or scheduled via Task Scheduler

echo 🔄 Starting Supabase ↔ Local Postgres sync...

REM Check if docker-compose is available
docker-compose version >nul 2>&1
if errorlevel 1 (
    echo ❌ docker-compose not found. Please install Docker Desktop or Docker Compose.
    exit /b 1
)

REM Check if containers are running
docker-compose ps | findstr "quantumtrade_backend" >nul
if errorlevel 1 (
    echo ⚠️  Backend container not running. Starting services...
    docker-compose up -d
    timeout /t 10 /nobreak >nul
)

REM Run sync service
echo 🚀 Executing sync service...
docker-compose exec backend python -m src.sync.sync_service

echo ✅ Sync completed successfully!