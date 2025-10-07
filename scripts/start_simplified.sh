#!/bin/bash

echo "🚀 Starting QuantumTrade stack..."
docker-compose up -d
echo "✅ QuantumTrade is now running at:"
echo "Frontend → http://localhost:5173"
echo "Backend → http://localhost:8000"