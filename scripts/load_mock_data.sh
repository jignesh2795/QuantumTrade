#!/bin/bash

# Script to generate and load mock data into local database
# Useful for backtesting and local development

echo "📊 Generating and seeding mock data into local DB..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Desktop or Docker Compose."
    exit 1
fi

# Check if containers are running
if ! docker-compose ps | grep -q "quantumtrade_backend"; then
    echo "⚠️  Backend container not running. Starting services..."
    docker-compose up -d
    sleep 10  # Wait for services to start
fi

# Run mock data loader
echo "🚀 Loading mock data..."
docker-compose exec backend python -m src.sync.mock_data_loader

echo "✅ Mock data loaded successfully!"