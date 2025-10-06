# QuantumTrade Docker Setup Verification

This document outlines the steps to verify that your QuantumTrade Docker setup is working correctly.

## 1. Directory Structure Verification

The docker directory should have the following structure:

```
docker/
├── docker-compose.yml
├── docker-compose.prod.yml
├── backend.Dockerfile
├── backend.Dockerfile.dev
├── frontend.Dockerfile
├── frontend.Dockerfile.dev
├── .dockerignore
└── README.md
```

## 2. Docker Compose Files Verification

### Development Configuration (docker-compose.yml)
- Uses development Dockerfiles
- Mounts volumes for live reload
- Exposes ports 8000 (backend) and 5173 (frontend)
- Uses uvicorn with --reload flag

### Production Configuration (docker-compose.prod.yml)
- Uses production Dockerfiles
- No volume mounts for live reload
- Exposes ports 8000 (backend) and 80 (frontend)
- Includes PostgreSQL database service

## 3. Dockerfile Verification

### Backend Dockerfiles
- Both install dependencies from requirements.txt
- Copy source code to /app/src
- Set environment variables
- Expose port 8000
- Development version uses --reload flag

### Frontend Dockerfiles
- Both install dependencies from package.json
- Copy source code to /app/src
- Copy public assets to /app/public
- Expose appropriate ports
- Development version runs npm run dev
- Production version builds and serves with Nginx

## 4. Testing the Setup

### Development Mode

1. Ensure Docker and Docker Compose are installed
2. Run from the project root:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```
3. Verify services:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:5173
   - API documentation: http://localhost:8000/docs

### Production Mode

1. Run from the project root:
   ```bash
   docker-compose -f docker/docker-compose.prod.yml up --build -d
   ```
2. Verify services:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost
   - Database: http://localhost:5432

## 5. Live Reload Testing

1. Start development services:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```
2. Make a change to a backend file in `backend/src/`
3. Observe the backend automatically restarts
4. Make a change to a frontend file in `frontend/src/`
5. Observe the frontend automatically reloads

## 6. Volume Mounting Verification

1. Start development services
2. Check that changes to files in:
   - `backend/src/` are reflected in the container
   - `frontend/src/` are reflected in the container
   - `frontend/public/` are reflected in the container
3. Verify that dependencies are cached in volumes:
   - `backend_cache` for Python packages
   - `frontend_cache` for Node modules

## 7. Cleanup Verification

1. Run the cleanup script:
   ```bash
   ./scripts/cleanup.sh
   ```
2. Verify that Docker resources are cleaned:
   - Stopped containers removed
   - Dangling images removed
   - Unused volumes removed
   - Unused networks removed
   - Builder cache cleaned

## 8. Expected Results

After successful Docker setup, you should be able to:

1. Access the frontend at http://localhost:5173 (dev) or http://localhost (prod)
2. Access the backend API at http://localhost:8000
3. See API documentation at http://localhost:8000/docs
4. Experience live reload during development
5. Have dependencies cached to avoid repeated downloads
6. Clean up resources to prevent disk overflow

## 9. Troubleshooting

### Common Issues:

1. **Port already in use**: Stop other services or change ports in docker-compose files
2. **Permission denied**: Ensure Docker is running with appropriate permissions
3. **Build failures**: Check that all required files are present
4. **Services not accessible**: Verify port mappings in docker-compose files

### Need Help?

Check the documentation in the `docker/README.md` file or refer to the main README.md for detailed instructions.