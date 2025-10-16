@echo off
echo ================================================
echo   Starting QuantumTrade Full Stack
echo ================================================

REM Kill existing processes
echo Cleaning up existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000"') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000"') do taskkill /F /PID %%a 2>nul

REM Start backend
echo.
echo Starting Backend API Server...
cd ..
start "QuantumTrade Backend" cmd /k python -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

REM Wait for backend
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start frontend
echo.
echo Starting Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

start "QuantumTrade Frontend" cmd /k npm run dev

echo.
echo ================================================
echo   QuantumTrade is running!
echo ================================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend UI:  http://localhost:3000
echo.
echo Press any key to exit...
pause >nul