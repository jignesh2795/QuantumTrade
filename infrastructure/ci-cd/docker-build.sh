#!/bin/bash

# QuantumTrade Docker Build Script

set -e

echo "Building QuantumTrade Docker images..."

# Build backend image
echo "Building backend image..."
docker build -t quantumtrade-backend -f backend/Dockerfile .

# Build frontend image
echo "Building frontend image..."
docker build -t quantumtrade-frontend -f frontend/Dockerfile .

echo "Docker images built successfully!"
echo "To run the application:"
echo "  docker-compose up"