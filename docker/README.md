# QuantumTrade Docker Setup

This directory contains all the Docker configuration files for the QuantumTrade project.

## Files

- `docker-compose.yml` - Development configuration with live reload
- `docker-compose.prod.yml` - Production configuration
- `backend.Dockerfile` - Production backend Dockerfile
- `backend.Dockerfile.dev` - Development backend Dockerfile
- `frontend.Dockerfile` - Production frontend Dockerfile
- `frontend.Dockerfile.dev` - Development frontend Dockerfile
- `.dockerignore` - Files and directories to ignore during Docker builds

## Usage

### Development

```bash
docker-compose -f docker/docker-compose.yml up --build
```

### Production

```bash
docker-compose -f docker/docker-compose.prod.yml up --build -d
```

## Services

- Backend: http://localhost:8000
- Frontend: http://localhost:5173 (dev) or http://localhost (prod)
- Database: http://localhost:5432 (prod only)