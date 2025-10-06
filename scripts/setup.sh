#!/bin/bash
# Install dependencies
set -e
echo "⚙️ Setting up QuantumTrade environment from root..."

# Backend
cd backend
python3 -m venv venv || echo "Venv exists"
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies installed"
cd ..

# Frontend
cd frontend
npm install
echo "✅ Frontend dependencies installed"
cd ..

echo "✅ Setup complete! Run ./scripts/start.sh to start the application"
echo "Or use Docker: docker-compose -f docker/docker-compose.yml up --build"