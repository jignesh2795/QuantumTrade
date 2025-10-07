#!/bin/bash

# QuantumTrade Start Script

set -e

echo "Starting QuantumTrade platform..."

# Run setup if needed
if [ ! -f .env ]; then
    echo "Running setup..."
    ./scripts/setup.sh
fi

# Start Docker Compose
echo "Starting Docker Compose..."
docker-compose up -d

echo "QuantumTrade platform started successfully!"
echo "Access the application at:"
echo "  Backend API: http://localhost:8000/docs"
echo "  Frontend: http://localhost:3000"
echo "  Database: PostgreSQL on port 5432"
