@echo off
echo Setting up QuantumTrade conda environment...

REM Check if conda is available
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Conda not found. Please install Miniconda or Anaconda first.
    echo Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM Create conda environment
echo Creating conda environment...
conda env create -f environment.yml

if %errorlevel% neq 0 (
    echo.
    echo Failed to create conda environment. This might be due to TA-Lib compilation issues.
    echo Trying alternative installation method...
    echo.
    
    REM Check if simplified environment works
    echo Trying simplified environment...
    conda env create -f environment_simple.yml
    
    if %errorlevel% neq 0 (
        echo.
        echo Failed to create simplified conda environment.
        echo Trying basic environment creation...
        echo.
        
        REM Create environment with Python only first
        conda create -n quantumtrade python=3.11 -y
        
        if %errorlevel% neq 0 (
            echo Failed to create basic environment.
            pause
            exit /b 1
        )
        
        REM Activate environment
        call conda activate quantumtrade
        
        if %errorlevel% neq 0 (
            echo Failed to activate conda environment.
            pause
            exit /b 1
        )
        
        REM Install packages one by one
        echo Installing core packages...
        conda install -c conda-forge pandas=2.1.4 numpy=1.26.2 sqlalchemy=2.0.23 aiohttp=3.9.1 pytest=7.4.3 -y
        
        if %errorlevel% neq 0 (
            echo Failed to install conda packages. Trying with pip...
            pip install pandas==2.1.4 numpy==1.26.2 sqlalchemy==2.0.23 aiohttp==3.9.1 pytest==7.4.3
        )
    ) else (
        REM Activate environment
        echo Activating simplified environment...
        call conda activate quantumtrade

        if %errorlevel% neq 0 (
            echo Failed to activate conda environment.
            pause
            exit /b 1
        )
        
        echo.
        echo Simplified environment created successfully.
        echo To install TA-Lib and pandas-ta, run:
        echo   install_ta_lib.bat
        echo.
    )
) else (
    REM Activate environment
    echo Activating environment...
    call conda activate quantumtrade

    if %errorlevel% neq 0 (
        echo Failed to activate conda environment.
        pause
        exit /b 1
    )
)

echo.
echo Setup complete!
echo To activate the environment in the future, run:
echo   conda activate quantumtrade
echo.
echo To run the application, execute:
echo   python main.py
echo.
echo If you encountered issues with TA-Lib, run:
echo   install_ta_lib.bat
echo.
pause