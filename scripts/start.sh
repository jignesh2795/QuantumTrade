#!/bin/bash
# Start app (local or Docker)
set -e
echo "🚀 Starting QuantumTrade from root..."

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if command -v docker-compose &> /dev/null; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose -f docker/docker-compose.yml up --build
else
    echo "⚙️ Starting locally..."
    
    # Start backend
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "✅ Backend virtual environment activated"
    else
        echo "⚠️ Backend virtual environment not found. Run ./scripts/setup.sh first"
        exit 1
    fi
    
    echo "🚀 Starting backend server on http://localhost:8000"
    uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload &
    cd ..
    
    # Start frontend
    cd frontend
    echo "🚀 Starting frontend on http://localhost:5173"
    npm run dev &
    cd ..
    
    echo "✅ QuantumTrade running locally!"
    echo "Frontend: http://localhost:5173"
    echo "Backend API: http://localhost:8000"
    echo "Press Ctrl+C to stop"
    
    # Wait for background processes
    wait
fi