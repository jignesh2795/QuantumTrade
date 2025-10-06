#!/bin/bash
# Test Docker Setup Script

echo "🧪 Testing QuantumTrade Docker Setup"

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if required files exist
required_files=(
    "docker-compose.yml"
    "docker-compose.prod.yml"
    "backend.Dockerfile"
    "backend.Dockerfile.dev"
    "frontend.Dockerfile"
    "frontend.Dockerfile.dev"
    ".dockerignore"
)

for file in "${required_files[@]}"; do
    if [ ! -f "docker/$file" ]; then
        echo "❌ Required file docker/$file not found"
        exit 1
    fi
done

echo "✅ All required Docker files are present"

# Check if backend requirements.txt exists
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ backend/requirements.txt not found"
    exit 1
fi

echo "✅ Backend requirements.txt found"

# Check if frontend package.json exists
if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json not found"
    exit 1
fi

echo "✅ Frontend package.json found"

# Test building the development images
echo "🏗️  Testing Docker build (this may take a few minutes)..."

# Build backend development image
if ! docker build -f docker/backend.Dockerfile.dev -t quantumtrade-backend-dev .; then
    echo "❌ Failed to build backend development image"
    exit 1
fi

echo "✅ Backend development image built successfully"

# Build frontend development image
if ! docker build -f docker/frontend.Dockerfile.dev -t quantumtrade-frontend-dev .; then
    echo "❌ Failed to build frontend development image"
    exit 1
fi

echo "✅ Frontend development image built successfully"

# Clean up test images
docker rmi quantumtrade-backend-dev quantumtrade-frontend-dev

echo "✅ Docker setup verification complete!"
echo "🚀 You can now run: docker-compose -f docker/docker-compose.yml up --build"