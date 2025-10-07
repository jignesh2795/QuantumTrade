#!/bin/bash

# QuantumTrade Docker Cleanup Script
# Cleans up old Docker artifacts to prevent disk filling up

echo "🧹 Cleaning unused Docker images, containers, and volumes..."
docker system prune -af --volumes
echo "✅ Cleanup complete!"
