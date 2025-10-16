#!/bin/bash

echo "Installing TA-Lib and pandas-ta for QuantumTrade..."

# Check if we're in the quantumtrade environment
if [[ $(conda info --envs | grep quantumtrade) == "" ]]; then
    echo "Please activate the quantumtrade environment first:"
    echo "  conda activate quantumtrade"
    exit 1
fi

# Try to install TA-Lib via conda first
echo "Attempting to install TA-Lib via conda..."
conda install -c conda-forge ta-lib -y

if [ $? -ne 0 ]; then
    echo ""
    echo "Conda installation failed. Trying pip installation..."
    echo ""
    
    # Check if we're on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo ""
        echo "macOS detected. Attempting to install via Homebrew..."
        echo ""
        
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            echo "Homebrew not found. Please install it first:"
            echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
        
        echo "Installing TA-Lib via Homebrew..."
        brew install ta-lib
        
        if [ $? -ne 0 ]; then
            echo "Failed to install TA-Lib via Homebrew."
            exit 1
        fi
        
        echo "Installing TA-Lib Python wrapper..."
        pip install TA-Lib
        
        if [ $? -ne 0 ]; then
            echo "Failed to install TA-Lib Python wrapper."
            exit 1
        fi
    else
        echo ""
        echo "Linux detected. Installing build dependencies..."
        echo ""
        
        # Try different package managers
        if command -v apt-get &> /dev/null; then
            echo "Installing dependencies via apt-get..."
            sudo apt-get update
            sudo apt-get install -y build-essential wget
        elif command -v yum &> /dev/null; then
            echo "Installing dependencies via yum..."
            sudo yum install -y gcc gcc-c++ make wget
        elif command -v dnf &> /dev/null; then
            echo "Installing dependencies via dnf..."
            sudo dnf install -y gcc gcc-c++ make wget
        else
            echo "Unsupported package manager. Please install build tools manually."
            exit 1
        fi
        
        echo "Downloading and compiling TA-Lib..."
        wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
        tar -xzf ta-lib-0.4.0-src.tar.gz
        cd ta-lib/
        ./configure --prefix=/usr
        make
        sudo make install
        cd ..
        
        echo "Installing TA-Lib Python wrapper..."
        pip install TA-Lib
        
        if [ $? -ne 0 ]; then
            echo "Failed to install TA-Lib Python wrapper."
            exit 1
        fi
    fi
else
    echo "TA-Lib installed successfully via conda."
fi

echo "Installing pandas-ta from GitHub..."
pip install git+https://github.com/twopirllc/pandas-ta.git

if [ $? -ne 0 ]; then
    echo "Failed to install pandas-ta."
    exit 1
fi

echo ""
echo "TA-Lib and pandas-ta installation process completed."