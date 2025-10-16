#!/bin/bash

echo "🚀 Starting QuantumTrade Full Stack"
echo "======================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Kill existing processes on ports
echo -e "${YELLOW}Cleaning up existing processes...${NC}"
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start backend API
echo -e "${BLUE}Starting Backend API Server...${NC}"
cd "$(dirname "$0")/.."
python -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend API started (PID: $BACKEND_PID)${NC}"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  Backend may not be ready yet${NC}"
fi

# Start frontend
echo -e "${BLUE}Starting Frontend...${NC}"
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo "======================================"
echo -e "${GREEN}🎉 QuantumTrade is running!${NC}"
echo "======================================"
echo ""
echo -e "${BLUE}Backend API:${NC}  http://localhost:8000"
echo -e "${BLUE}API Docs:${NC}     http://localhost:8000/docs"
echo -e "${BLUE}Frontend UI:${NC}  http://localhost:3000"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Handle Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait