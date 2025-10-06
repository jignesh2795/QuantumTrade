@echo off
REM Test Docker Setup Script

echo 🧪 Testing QuantumTrade Docker Setup

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Check if required files exist
if not exist "docker\docker-compose.yml" (
    echo ❌ Required file docker\docker-compose.yml not found
    exit /b 1
)

if not exist "docker\docker-compose.prod.yml" (
    echo ❌ Required file docker\docker-compose.prod.yml not found
    exit /b 1
)

if not exist "docker\backend.Dockerfile" (
    echo ❌ Required file docker\backend.Dockerfile not found
    exit /b 1
)

if not exist "docker\backend.Dockerfile.dev" (
    echo ❌ Required file docker\backend.Dockerfile.dev not found
    exit /b 1
)

if not exist "docker\frontend.Dockerfile" (
    echo ❌ Required file docker\frontend.Dockerfile not found
    exit /b 1
)

if not exist "docker\frontend.Dockerfile.dev" (
    echo ❌ Required file docker\frontend.Dockerfile.dev not found
    exit /b 1
)

if not exist "docker\.dockerignore" (
    echo ❌ Required file docker\.dockerignore not found
    exit /b 1
)

echo ✅ All required Docker files are present

REM Check if backend requirements.txt exists
if not exist "backend\requirements.txt" (
    echo ❌ backend\requirements.txt not found
    exit /b 1
)

echo ✅ Backend requirements.txt found

REM Check if frontend package.json exists
if not exist "frontend\package.json" (
    echo ❌ frontend\package.json not found
    exit /b 1
)

echo ✅ Frontend package.json found

echo 🚀 Docker setup verification complete!
echo You can now run: docker-compose -f docker\docker-compose.yml up --build