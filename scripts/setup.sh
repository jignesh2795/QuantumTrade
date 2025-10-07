#!/bin/bash

# QuantumTrade Setup Script

set -e

echo "Setting up QuantumTrade platform..."

# Create logs directory
mkdir -p logs

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Setup database
echo "Setting up database..."
python scripts/setup/database_setup.py

# Seed database with sample data
echo "Seeding database with sample data..."
python scripts/setup/seed_data.py

echo "QuantumTrade setup completed successfully!"
echo "To start the application, run: docker-compose up"