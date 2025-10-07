@echo off
REM QuantumTrade Setup Script for Windows

echo Setting up QuantumTrade platform...

REM Create logs directory
if not exist "logs" mkdir logs

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from .env.example...
    copy .env.example .env
)

REM Setup database
echo Setting up database...
python scripts\setup\database_setup.py

REM Seed database with sample data
echo Seeding database with sample data...
python scripts\setup\seed_data.py

echo QuantumTrade setup completed successfully!
echo To start the application, run: docker-compose up