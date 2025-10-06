# QuantumTrade Setup Verification

This document outlines the steps to verify that your QuantumTrade setup is working correctly.

## 1. Directory Structure Verification

The project should have the following structure:

```
quantumtrade/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
├── scripts/
│   ├── start.sh
│   ├── setup.sh
│   └── cleanup.sh
├── frontend/
├── backend/
├── docker/
```

## 2. Backend Verification

### Files to Check:
- `backend/src/main.py` - FastAPI entry point
- `backend/src/api/server.py` - FastAPI app with CORS
- `backend/src/api/routes/__init__.py` - API routes
- `backend/requirements.txt` - Dependencies

### Verification Steps:
1. Navigate to the backend directory
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python src/main.py`
6. Verify the server is running at http://localhost:8000

## 3. Frontend Verification

### Files to Check:
- `frontend/src/main.jsx` - React entry point
- `frontend/src/App.jsx` - Main application component
- `frontend/package.json` - Dependencies
- `frontend/public/index.html` - HTML template

### Verification Steps:
1. Navigate to the frontend directory
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Verify the frontend is running at http://localhost:5173

## 4. Scripts Verification

### Files to Check:
- `scripts/setup.sh` - Dependency installation
- `scripts/start.sh` - Application startup
- `scripts/cleanup.sh` - Docker cleanup

### Verification Steps:
1. Make scripts executable: `chmod +x scripts/*.sh`
2. Run setup: `./scripts/setup.sh`
3. Start application: `./scripts/start.sh`
4. Clean up: `./scripts/cleanup.sh`

## 5. Docker Verification

### Files to Check:
- `docker/docker-compose.yml` - Docker Compose configuration
- `backend/Dockerfile` - Backend production Dockerfile
- `backend/Dockerfile.dev` - Backend development Dockerfile
- `frontend/Dockerfile` - Frontend production Dockerfile
- `frontend/Dockerfile.dev` - Frontend development Dockerfile

### Verification Steps:
1. Ensure Docker and Docker Compose are installed
2. Run: `docker-compose -f docker/docker-compose.yml up --build`
3. Verify services are running:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173
   - Database: localhost:5432

## 6. Testing Verification

### Backend Tests:
1. Navigate to the backend directory
2. Activate virtual environment
3. Run: `pytest`

## 7. Expected Results

After successful setup, you should be able to:

1. Access the frontend at http://localhost:5173
2. Access the backend API at http://localhost:8000
3. See API documentation at http://localhost:8000/docs
4. Run tests successfully
5. Build and run Docker containers

## 8. Troubleshooting

### Common Issues:

1. **Port already in use**: Change ports in docker-compose.yml and .env
2. **Permission denied**: Make scripts executable with `chmod +x`
3. **Module not found**: Ensure virtual environment is activated
4. **Docker not found**: Install Docker Desktop

### Need Help?

Check the documentation in the `docs/` directory or refer to the SETUP_GUIDE.md for detailed instructions.