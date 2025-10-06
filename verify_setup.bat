@echo off
REM Verification script for QuantumTrade setup

echo 🔍 Verifying QuantumTrade setup...

REM Check if quantumtrade directory exists
if not exist "quantumtrade" (
    echo ❌ quantumtrade directory not found
    exit /b 1
)

echo ✅ quantumtrade directory exists

REM Check key files
if not exist "quantumtrade\README.md" (
    echo ❌ Required file quantumtrade\README.md not found
    exit /b 1
)

if not exist "quantumtrade\backend\requirements.txt" (
    echo ❌ Required file quantumtrade\backend\requirements.txt not found
    exit /b 1
)

if not exist "quantumtrade\frontend\package.json" (
    echo ❌ Required file quantumtrade\frontend\package.json not found
    exit /b 1
)

if not exist "quantumtrade\backend\src\main.py" (
    echo ❌ Required file quantumtrade\backend\src\main.py not found
    exit /b 1
)

if not exist "quantumtrade\backend\src\api\server.py" (
    echo ❌ Required file quantumtrade\backend\src\api\server.py not found
    exit /b 1
)

if not exist "quantumtrade\backend\src\api\routes\__init__.py" (
    echo ❌ Required file quantumtrade\backend\src\api\routes\__init__.py not found
    exit /b 1
)

if not exist "quantumtrade\frontend\src\main.jsx" (
    echo ❌ Required file quantumtrade\frontend\src\main.jsx not found
    exit /b 1
)

if not exist "quantumtrade\frontend\src\App.jsx" (
    echo ❌ Required file quantumtrade\frontend\src\App.jsx not found
    exit /b 1
)

if not exist "quantumtrade\scripts\setup.sh" (
    echo ❌ Required file quantumtrade\scripts\setup.sh not found
    exit /b 1
)

if not exist "quantumtrade\scripts\start.sh" (
    echo ❌ Required file quantumtrade\scripts\start.sh not found
    exit /b 1
)

if not exist "quantumtrade\scripts\cleanup.sh" (
    echo ❌ Required file quantumtrade\scripts\cleanup.sh not found
    exit /b 1
)

echo ✅ All key files present

REM Check Git initialization
cd quantumtrade
if not exist ".git" (
    echo ❌ Git repository not initialized
    exit /b 1
)

echo ✅ Git repository initialized

echo 🎉 QuantumTrade setup verification complete!
echo Run 'quantumtrade\scripts\start.sh' to start the app.