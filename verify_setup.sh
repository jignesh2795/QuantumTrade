#!/bin/bash
# Verification script for QuantumTrade setup

echo "🔍 Verifying QuantumTrade setup..."

# Check if quantumtrade directory exists
if [ ! -d "quantumtrade" ]; then
    echo "❌ quantumtrade directory not found"
    exit 1
fi

echo "✅ quantumtrade directory exists"

# Check key files
key_files=(
    "quantumtrade/README.md"
    "quantumtrade/backend/requirements.txt"
    "quantumtrade/frontend/package.json"
    "quantumtrade/backend/src/main.py"
    "quantumtrade/backend/src/api/server.py"
    "quantumtrade/backend/src/api/routes/__init__.py"
    "quantumtrade/frontend/src/main.jsx"
    "quantumtrade/frontend/src/App.jsx"
    "quantumtrade/scripts/setup.sh"
    "quantumtrade/scripts/start.sh"
    "quantumtrade/scripts/cleanup.sh"
)

for file in "${key_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file $file not found"
        exit 1
    fi
done

echo "✅ All key files present"

# Check Git initialization
cd quantumtrade
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized"
    exit 1
fi

echo "✅ Git repository initialized"

# Check branches
git_branches=$(git branch)
if [[ $git_branches != *"main"* ]]; then
    echo "❌ main branch not found"
    exit 1
fi

if [[ $git_branches != *"develop"* ]]; then
    echo "❌ develop branch not found"
    exit 1
fi

echo "✅ Git branches (main, develop) created"

# Check initial commit
if [ -z "$(git log --oneline -1)" ]; then
    echo "❌ Initial commit not found"
    exit 1
fi

echo "✅ Initial commit created"

echo "🎉 QuantumTrade setup verification complete!"
echo "Run './quantumtrade/scripts/start.sh' to start the app."