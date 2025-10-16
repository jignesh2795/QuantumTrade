@echo off
echo Installing TA-Lib and pandas-ta for QuantumTrade...

REM Check if we're in the quantumtrade environment
conda info --envs | findstr quantumtrade >nul
if %errorlevel% neq 0 (
    echo Please activate the quantumtrade environment first:
    echo   conda activate quantumtrade
    pause
    exit /b 1
)

REM Try to install TA-Lib via conda first
echo Attempting to install TA-Lib via conda...
conda install -c conda-forge ta-lib -y

if %errorlevel% neq 0 (
    echo.
    echo Conda installation failed. Trying pip installation...
    echo.
    
    REM Check if we're on Windows
    echo %OS% | findstr Windows >nul
    if %errorlevel% equ 0 (
        echo.
        echo Windows detected. Attempting to install pre-compiled wheel...
        echo.
        
        REM Try to download and install the pre-compiled wheel
        echo Please download the appropriate TA-Lib wheel from:
        echo https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
        echo.
        echo After downloading, install it with:
        echo pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl
        echo (adjust filename as needed for your Python version)
        echo.
    ) else (
        echo.
        echo Non-Windows system detected.
        echo Please install TA-Lib dependencies first:
        echo.
        echo Ubuntu/Debian:
        echo   sudo apt-get update
        echo   sudo apt-get install build-essential wget
        echo   wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
        echo   tar -xzf ta-lib-0.4.0-src.tar.gz
        echo   cd ta-lib/
        echo   ./configure --prefix=/usr
        echo   make
        echo   sudo make install
        echo   cd ..
        echo   pip install TA-Lib
        echo.
        echo macOS:
        echo   brew install ta-lib
        echo   pip install TA-Lib
        echo.
    )
) else (
    echo TA-Lib installed successfully via conda.
)

echo Installing pandas-ta from GitHub...
pip install git+https://github.com/twopirllc/pandas-ta.git

if %errorlevel% neq 0 (
    echo Failed to install pandas-ta.
    pause
    exit /b 1
)

echo.
echo TA-Lib and pandas-ta installation process completed.
echo.
pause