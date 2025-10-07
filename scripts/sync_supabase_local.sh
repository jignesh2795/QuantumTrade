#!/bin/bash

# Script to sync data between Supabase and local Postgres mirror
# Can be run manually or scheduled via cron

echo "🔄 Starting Supabase ↔ Local Postgres sync..."

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

# Run sync service
echo "🚀 Executing sync service..."
docker-compose exec backend python -m src.sync.sync_service

echo "✅ Sync completed successfully!"