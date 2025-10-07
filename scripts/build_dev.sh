#!/bin/bash

# Build development Docker images for QuantumTrade

echo "Building development Docker images..."

# Build backend development image
echo "Building backend development image..."
docker build -f backend/Dockerfile.dev -t quantumtrade-backend-dev .

# Build frontend development image
echo "Building frontend development image..."
docker build -f frontend/Dockerfile.dev -t quantumtrade-frontend-dev .

echo "Development images built successfully!"