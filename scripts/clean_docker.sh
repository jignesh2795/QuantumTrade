#!/bin/bash

# Clean Docker script for QuantumTrade
# Clears unused images/volumes safely

echo "Cleaning up Docker resources..."

# Remove stopped containers
echo "Removing stopped containers..."
docker container prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

# Remove unused images
echo "Removing unused images..."
docker image prune -f

# Remove unused build cache
echo "Removing build cache..."
docker builder prune -f

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

echo "Docker cleanup completed!"