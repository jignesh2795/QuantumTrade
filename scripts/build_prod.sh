#!/bin/bash

# Build production Docker images for QuantumTrade

echo "Building production Docker images..."

# Build backend production image
echo "Building backend production image..."
docker build -f backend/Dockerfile -t quantumtrade-backend .

# Build frontend production image
echo "Building frontend production image..."
docker build -f frontend/Dockerfile -t quantumtrade-frontend .

echo "Production images built successfully!"