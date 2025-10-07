@echo off
REM Script to generate and load mock data into local database
REM Useful for backtesting and local development

echo 📊 Generating and seeding mock data into local DB...

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

REM Run mock data loader
echo 🚀 Loading mock data...
docker-compose exec backend python -m src.sync.mock_data_loader

echo ✅ Mock data loaded successfully!