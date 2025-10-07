@echo off
REM QuantumTrade Start Script for Windows

echo Starting QuantumTrade platform...

REM Run setup if needed
if not exist ".env" (
    echo Running setup...
    call scripts\setup.bat
)

REM Start Docker Compose
echo Starting Docker Compose...
docker-compose up -d

echo QuantumTrade platform started successfully!
echo Access the application at:
echo   Backend API: http://localhost:8000/docs
echo   Frontend: http://localhost:3000
echo   Database: PostgreSQL on port 5432