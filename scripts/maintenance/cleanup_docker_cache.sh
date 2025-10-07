#!/bin/bash

# QuantumTrade Docker Cache Cleanup Script

echo "Cleaning unused Docker images, volumes, and cache..."
docker system prune -af
docker volume prune -f
docker builder prune -af
echo "Cleanup complete!"
