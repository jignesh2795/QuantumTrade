#!/bin/bash

echo "Setting up QuantumTrade conda environment..."

# Check if conda is available
if ! command -v conda &> /dev/null
then
    echo "Conda not found. Please install Miniconda or Anaconda first."
    echo "Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create conda environment
echo "Creating conda environment..."
conda env create -f environment.yml

if [ $? -ne 0 ]; then
    echo ""
    echo "Failed to create conda environment. This might be due to TA-Lib compilation issues."
    echo "Trying alternative installation method..."
    echo ""
    
    # Create environment with Python only first
    conda create -n quantumtrade python=3.11 -y
    
    if [ $? -ne 0 ]; then
        echo "Failed to create basic environment."
        exit 1
    fi
    
    # Activate environment
    conda activate quantumtrade
    
    if [ $? -ne 0 ]; then
        echo "Failed to activate conda environment."
        exit 1
    fi
    
    # Install packages one by one
    echo "Installing core packages..."
    conda install -c conda-forge pandas=2.1.4 numpy=1.26.2 sqlalchemy=2.0.23 aiohttp=3.9.1 pytest=7.4.3 ta-lib -y
    
    if [ $? -ne 0 ]; then
        echo "Failed to install conda packages. Trying with pip..."
        pip install pandas==2.1.4 numpy==1.26.2 sqlalchemy==2.0.23 aiohttp==3.9.1 pytest==7.4.3
    fi
    
    echo "Installing pip packages..."
    pip install python-dotenv==1.0.0 pydantic==2.5.0 pydantic-settings==2.1.0 aiosqlite==0.19.0 alembic==1.13.0 fastapi==0.108.0 uvicorn[standard]==0.25.0 websockets==12.0 pandas-ta pytest-asyncio==0.21.1 pytest-cov==4.1.0 black==23.12.1 ruff==0.1.9 mypy==1.7.1
    
    if [ $? -ne 0 ]; then
        echo "Failed to install pip packages."
        exit 1
    fi
else
    # Activate environment
    echo "Activating environment..."
    conda activate quantumtrade
    
    if [ $? -ne 0 ]; then
        echo "Failed to activate conda environment."
        exit 1
    fi
fi

echo ""
echo "Setup complete!"
echo "To activate the environment in the future, run:"
echo "  conda activate quantumtrade"
echo ""
echo "To run the application, execute:"
echo "  python main.py"