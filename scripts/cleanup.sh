#!/bin/bash
# Docker cleanup
echo "🧹 Cleaning up Docker containers, images, volumes..."
docker container prune -f
docker image prune -f
docker volume prune -f
docker network prune -f
docker builder prune -a --filter "until=72h" -f
echo "✅ Cleanup complete!"