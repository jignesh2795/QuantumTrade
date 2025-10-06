# Complete QuantumTrade Setup Guide

This guide covers all aspects of setting up the QuantumTrade project for development, testing, and production.

## 1. Dependency & Environment Management

### Python Dependencies
All Python dependencies are pinned in `backend/requirements.txt` to avoid future conflicts:
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

### Node Dependencies
Frontend dependencies are pinned in `frontend/package.json`:
```json
{
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

### Environment Variables
Use `.env` files for secrets and configuration:
- Never commit `.env` files to Git
- Use `.env.example` as a template
- Each environment (dev, test, prod) can have its own `.env` file

## 2. Database Setup

### Dockerized Database with Persistent Volumes
The database is configured in `docker/docker-compose.yml` with persistent volumes:
```yaml
db:
  image: postgres:15
  environment:
    POSTGRES_USER: quantumtrade
    POSTGRES_PASSWORD: quantumtrade
    POSTGRES_DB: quantumtrade
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

### Migrations
Database migrations are managed using SQLAlchemy:
- Migration files are stored in `backend/src/database/migrations/versions/`
- Use Alembic-like structure for version control
- Each migration has upgrade and downgrade functions

### Seed Data
Sample data for development/testing is available in `backend/src/database/seed_data.py`:
- Portfolio sample data
- Trade sample data
- Market data sample

## 3. Docker / Storage Optimization

### Volume Mounts
Docker configuration uses volume mounts to avoid rebuilding dependencies:
```yaml
volumes:
  - ../backend/src:/app/src
  - backend_cache:/root/.cache/pip
  - ../frontend/src:/app/src
  - ../frontend/public:/app/public
  - frontend_cache:/app/node_modules
```

### Multi-stage Builds
Production Dockerfiles use multi-stage builds to reduce image size:
- Backend: Build stage installs dependencies, final stage copies only necessary files
- Frontend: Build stage compiles assets, final stage serves with Nginx

### Cleanup Script
Regular cleanup prevents disk overflow:
```bash
./scripts/cleanup.sh
```
This removes unused containers, images, volumes, and builder cache.

## 4. Logging & Monitoring

### Centralized Logging
- Backend logs are written to `logs/backend.log`
- Frontend console logs are available in browser dev tools
- Log rotation prevents huge disk usage

### Configuration
Logging is configured in `backend/src/config/logging_config.yaml`:
- Console output for development
- File output with rotation for production
- Different log levels for different environments

## 5. Testing Framework

### Test Structure
Tests are organized in `backend/tests/`:
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- End-to-end tests in `tests/e2e/`

### Fixtures and Mocks
- Sample data fixtures in `tests/fixtures/sample_data.py`
- Mock services in `tests/fixtures/mock_services.py`
- Avoid hitting real APIs during testing

### CI/CD Integration
GitHub Actions workflow in `.github/workflows/ci.yml`:
- Runs tests on push and pull request
- Builds Docker images
- Ensures code quality

## 6. Security

### HTTPS
Production deployment uses Nginx reverse proxy for HTTPS termination.

### Input Validation
Security utilities in `backend/src/config/security.py`:
- Password hashing and verification
- API key generation
- Input sanitization
- Symbol validation

### Authentication
JWT-based authentication:
- Configurable secret and algorithm
- Token expiration settings
- Secure header transmission

## 7. Scalability

### Agent Architecture
Agents are designed for easy extension:
- Plugin system in `backend/src/agents/plugins/`
- Configuration in `backend/src/config/scalability.py`
- Enable/disable agents via environment variables

### Async Processing
Asynchronous task processing:
- Queue configuration for heavy computations
- Worker scaling based on load
- Microservice architecture support

### Service Scaling
Configuration for horizontal scaling:
- Database connection pooling
- API rate limiting
- Load balancing settings

## 8. Developer Experience

### Root-Run Scripts
All operations can be performed from the root directory:
- `./scripts/setup.sh` - Install dependencies
- `./scripts/start.sh` - Start application
- `./scripts/cleanup.sh` - Clean Docker resources

### Consistent Formatting
- `.editorconfig` for consistent coding styles
- VSCode settings for automatic formatting
- Python Black formatter
- Prettier for JavaScript/JSON

### Git Best Practices
- Comprehensive `.gitignore`
- Branching strategy (main, develop, feature/*)
- Semantic commit messages
- Version tagging

## Quick Start

1. Run the setup script:
   ```bash
   chmod +x setup_quantumtrade.sh
   ./setup_quantumtrade.sh
   ```

2. Initialize Git:
   ```bash
   cd quantumtrade
   git init
   git checkout -b main
   git checkout -b develop
   git add .
   git commit -m "Initial setup"
   ```

3. Start the application:
   ```bash
   ./scripts/start.sh
   ```

This setup ensures the project is:
- ✅ Stable for local development
- ✅ Docker-friendly
- ✅ Scalable & maintainable
- ✅ Ready for production deployment