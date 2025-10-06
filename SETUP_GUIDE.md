# QuantumTrade – Full From-Scratch Setup Instructions

## 1️⃣ Clone the Repository

```bash
git clone <your-repo-url> quantumtrade
cd quantumtrade
```

## 2️⃣ Generate Project Skeleton

If you don't have the folder structure yet, use the skeleton generator:

Save this as generate_skeleton.sh:

```bash
#!/bin/bash
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

echo "✅ QuantumTrade skeleton created!"
```

Run it:

```bash
chmod +x generate_skeleton.sh
./generate_skeleton.sh
```

## 3️⃣ Populate Placeholder Files

### Backend:

- `backend/src/main.py` → FastAPI Uvicorn runner
- `backend/src/api/server.py` → FastAPI app
- `backend/src/api/routes/__init__.py` → /health & /agents
- `backend/src/core/__init__.py` → placeholder
- `backend/src/utils/__init__.py` → placeholder

### Frontend:

- `frontend/src/main.jsx` → ReactDOM render
- `frontend/src/App.jsx` → Placeholder component
- `frontend/public/index.html` → Basic HTML shell

### Scripts:

- `scripts/setup.sh` → Install dependencies
- `scripts/start.sh` → Start app (local or Docker)
- `scripts/cleanup.sh` → Docker cleanup

## 4️⃣ Install Dependencies

### Backend (requirements.txt):

```
fastapi==0.111.1
uvicorn[standard]==0.23.2
sqlalchemy==2.0.22
psycopg2-binary==2.9.7
pydantic==2.6.0
python-dotenv==1.0.1
pytest==8.2.1
pytest-asyncio==0.22.0
requests==2.32.1
numpy==1.26.2
pandas==2.1.1
aiohttp==3.9.3
```

### Frontend (package.json):

```json
{
  "name": "quantumtrade-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.5",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "react-router-dom": "^6.17.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.0",
    "vite": "^4.6.14"
  }
}
```

### Install:

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..
```

## 5️⃣ Start QuantumTrade

```bash
./scripts/start.sh
```

- Local dev: backend http://localhost:8000, frontend http://localhost:5173
- Docker: automatically builds containers and mounts volumes

## 6️⃣ Cleanup Old Docker Files (Prevent Disk Overflow)

```bash
./scripts/cleanup.sh
```

Removes unused containers, images, volumes, and builder cache older than 72h

## ✅ Now You Can

1. Clone repo
2. Generate skeleton (if needed)
3. Populate placeholder files
4. Install dependencies
5. Run app from root (`./scripts/start.sh`)

Your project is fully structured, Docker-ready, dependency-cached, and root-run capable.