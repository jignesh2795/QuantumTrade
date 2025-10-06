#!/bin/bash
# QuantumTrade Skeleton Generator

echo "🚀 Generating QuantumTrade project skeleton..."

# Create directory structure
mkdir -p quantumtrade/{docs,scripts,frontend/{src/{features,components,hooks,context,services,utils},public/assets},backend/{src/{core,services,agents/plugins,api/{routes,middleware},database/migrations,config/environments,utils},tests,scripts},docker}

# Create empty files
touch quantumtrade/README.md
touch quantumtrade/LICENSE
touch quantumtrade/.gitignore
touch quantumtrade/.env.example

# Docs
for f in setup api architecture deployment troubleshooting; do
    touch quantumtrade/docs/$f.md
done

# Scripts
for s in start setup cleanup; do
    touch quantumtrade/scripts/$s.sh
done

# Frontend
touch quantumtrade/frontend/Dockerfile
touch quantumtrade/frontend/Dockerfile.dev
touch quantumtrade/frontend/package.json
touch quantumtrade/frontend/vite.config.js
touch quantumtrade/frontend/src/main.jsx
touch quantumtrade/frontend/src/App.jsx
touch quantumtrade/frontend/public/index.html

# Backend
touch quantumtrade/backend/Dockerfile
touch quantumtrade/backend/Dockerfile.dev
touch quantumtrade/backend/requirements.txt
touch quantumtrade/backend/src/__init__.py
touch quantumtrade/backend/src/main.py
touch quantumtrade/backend/src/core/__init__.py
touch quantumtrade/backend/src/services/__init__.py
touch quantumtrade/backend/src/agents/__init__.py
touch quantumtrade/backend/src/agents/plugins/__init__.py
touch quantumtrade/backend/src/api/server.py
touch quantumtrade/backend/src/api/routes/__init__.py
touch quantumtrade/backend/src/api/middleware/__init__.py
touch quantumtrade/backend/src/database/migrations/__init__.py
touch quantumtrade/backend/src/config/environments/development.yaml
touch quantumtrade/backend/src/config/feature_flags.yaml
touch quantumtrade/backend/src/utils/__init__.py
touch quantumtrade/backend/tests/__init__.py
touch quantumtrade/backend/scripts/db_migrate.sh

# Docker folder
touch quantumtrade/docker/docker-compose.yml
touch quantumtrade/docker/.dockerignore

echo "✅ QuantumTrade skeleton created successfully!"