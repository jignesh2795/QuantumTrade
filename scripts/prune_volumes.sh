#!/bin/bash

# QuantumTrade Volume Pruning Script
# Removes unused Docker volumes to free up disk space

echo "🧹 Pruning unused Docker volumes..."

# Remove all unused local volumes
docker volume prune -f

# Remove dangling volumes specifically
docker volume rm $(docker volume ls -qf dangling=true) 2>/dev/null || true

echo "✅ Volume pruning complete!"