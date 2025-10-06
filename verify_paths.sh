#!/bin/bash
# Verify that all scripts point to the correct directories

echo "🔍 Verifying script paths..."

# Check if we're in the correct directory
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Check setup scripts
echo -e "\n📁 Checking setup scripts..."
if [ -f "scripts/setup.sh" ]; then
    echo "✅ scripts/setup.sh exists"
    echo "Contents:"
    cat scripts/setup.sh
else
    echo "❌ scripts/setup.sh not found"
fi

if [ -f "scripts/start.sh" ]; then
    echo -e "\n✅ scripts/start.sh exists"
    echo "Contents:"
    cat scripts/start.sh
else
    echo -e "\n❌ scripts/start.sh not found"
fi

if [ -f "scripts/cleanup.sh" ]; then
    echo -e "\n✅ scripts/cleanup.sh exists"
    echo "Contents:"
    cat scripts/cleanup.sh
else
    echo -e "\n❌ scripts/cleanup.sh not found"
fi

# Check if main directories exist
echo -e "\n📂 Checking main directories..."
if [ -d "backend" ]; then
    echo "✅ backend directory exists"
else
    echo "❌ backend directory not found"
fi

if [ -d "frontend" ]; then
    echo "✅ frontend directory exists"
else
    echo "❌ frontend directory not found"
fi

if [ -d "docker" ]; then
    echo "✅ docker directory exists"
else
    echo "❌ docker directory not found"
fi

if [ -d "scripts" ]; then
    echo "✅ scripts directory exists"
else
    echo "❌ scripts directory not found"
fi

echo -e "\n✅ Path verification complete!"