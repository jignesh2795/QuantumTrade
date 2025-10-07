#!/bin/bash

# Start full stack locally for QuantumTrade

echo "Starting QuantumTrade local development stack..."

# Start Docker Compose services
echo "Starting Docker services..."
docker-compose up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo "QuantumTrade local stack started!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000"