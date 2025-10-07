# Deployment Guide

## 🎯 Deployment Targets

QuantumTrade can be deployed to various cloud platforms:

-   **Render** - Simple deployment with automatic SSL
-   **Railway** - Developer-first infrastructure platform
-   **Fly.io** - Global application deployment
-   **DigitalOcean** - Cloud infrastructure provider
-   **Supabase** - Backend-as-a-Service with database
-   **Vercel** - Frontend deployment platform

## 🐳 Docker Deployment

### Build Docker Images

```bash
# Build backend image
docker build -t quantumtrade-backend -f backend/Dockerfile .

# Build frontend image
docker build -t quantumtrade-frontend -f frontend/Dockerfile .
```

### Run with Docker Compose

```bash
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

### Push to Container Registry

```bash
# Tag images
docker tag quantumtrade-backend ghcr.io/your-username/quantumtrade-backend:latest
docker tag quantumtrade-frontend ghcr.io/your-username/quantumtrade-frontend:latest

# Push to GitHub Container Registry
docker push ghcr.io/your-username/quantumtrade-backend:latest
docker push ghcr.io/your-username/quantumtrade-frontend:latest
```

## ☁️ Cloud Provider Deployment

### Render Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure environment variables:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_ANON_KEY=your_anon_key
    DATABASE_URL=your_database_url
    ```
4. Set build command:
    ```bash
    pip install -r backend/requirements.txt
    ```
5. Set start command:
    ```bash
    uvicorn backend.src.main:app --host 0.0.0.0 --port $PORT
    ```

### Railway Deployment

1. Install Railway CLI:

    ```bash
    npm install -g @railway/cli
    ```

2. Login to Railway:

    ```bash
    railway login
    ```

3. Create a new project:

    ```bash
    railway init
    ```

4. Deploy:
    ```bash
    railway up
    ```

### Fly.io Deployment

1. Install Fly CLI:

    ```bash
    curl -L https://fly.io/install.sh | sh
    ```

2. Create Fly app:

    ```bash
    flyctl launch
    ```

3. Deploy:
    ```bash
    flyctl deploy
    ```

### DigitalOcean Deployment

1. Create a new App on DigitalOcean
2. Connect your GitHub repository
3. Configure environment variables
4. Set build and run commands
5. Deploy the app

## 🌐 Frontend Deployment (Vercel)

### Deploy to Vercel

1. Install Vercel CLI:

    ```bash
    npm install -g vercel
    ```

2. Login to Vercel:

    ```bash
    vercel login
    ```

3. Deploy frontend:
    ```bash
    cd frontend
    vercel --prod
    ```

### Vercel Configuration

Create `vercel.json` in the frontend directory:

```json
{
    "version": 2,
    "builds": [
        {
            "src": "package.json",
            "use": "@vercel/static-build",
            "config": {
                "distDir": "dist"
            }
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "/index.html"
        }
    ]
}
```

## 🔐 Environment Configuration

### Production Environment Variables

Set the following environment variables in your deployment platform:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Application Settings
SECRET_KEY=your_secret_key
DEBUG=False
PORT=8000

# AI/ML Settings
MODEL_PATH=./models

# Backtesting Settings
BACKTEST_DATA_PATH=./data
```

### Secret Management

Use your deployment platform's secret management features:

-   **GitHub Secrets** for GitHub Actions
-   **Render Environment Variables** for Render
-   **Railway Variables** for Railway
-   **Fly Secrets** for Fly.io
-   **DigitalOcean App Platform Variables** for DigitalOcean

## 🔄 Continuous Deployment

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
    push:
        branches: [main]

jobs:
    deploy:
        runs-on: ubuntu-latest

        steps:
            - name: Checkout code
              uses: actions/checkout@v3

            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                  python-version: "3.11"

            - name: Install dependencies
              run: |
                  cd backend
                  pip install -r requirements.txt

            - name: Run tests
              run: |
                  cd backend
                  pytest

            - name: Build Docker images
              run: |
                  docker build -t quantumtrade-backend -f backend/Dockerfile .
                  docker build -t quantumtrade-frontend -f frontend/Dockerfile .

            - name: Push to container registry
              run: |
                  echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
                  docker tag quantumtrade-backend ghcr.io/${{ github.repository }}/quantumtrade-backend:latest
                  docker tag quantumtrade-frontend ghcr.io/${{ github.repository }}/quantumtrade-frontend:latest
                  docker push ghcr.io/${{ github.repository }}/quantumtrade-backend:latest
                  docker push ghcr.io/${{ github.repository }}/quantumtrade-frontend:latest

            - name: Deploy to Render
              run: |
                  # Add deployment commands for your chosen platform
```

## 📊 Monitoring and Observability

### Health Checks

Implement health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health/database")
async def database_health_check(db = Depends(get_db)):
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {"status": "database_healthy"}
    except Exception as e:
        return {"status": "database_unhealthy", "error": str(e)}
```

### Logging

Configure structured logging:

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

# Configure logger
logger = logging.getLogger("quantumtrade")
logger.setLevel(logging.INFO)
```

### Metrics

Implement Prometheus metrics:

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(time.time() - start_time)

    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🔒 Security Considerations

### HTTPS Configuration

Ensure all deployments use HTTPS:

-   Use automatic SSL certificates from your deployment platform
-   Redirect HTTP traffic to HTTPS
-   Use secure headers

### CORS Configuration

Configure CORS properly:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Rate Limiting

Implement rate limiting to prevent abuse:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("100/minute")
async def get_data(request: Request):
    return {"data": "sensitive_data"}
```

## 🧪 Testing in Production

### Smoke Tests

Run smoke tests after deployment:

```bash
#!/bin/bash
# smoke_test.sh

# Test backend health endpoint
curl -f https://your-backend-url/health || exit 1

# Test frontend
curl -f https://your-frontend-url/ || exit 1

# Test API endpoint
curl -f https://your-backend-url/api/trades || exit 1

echo "All smoke tests passed!"
```

### Rollback Procedures

Implement rollback procedures:

```bash
#!/bin/bash
# rollback.sh

# Rollback to previous version
kubectl rollout undo deployment/quantumtrade-backend
kubectl rollout undo deployment/quantumtrade-frontend

# Verify rollback
kubectl rollout status deployment/quantumtrade-backend
kubectl rollout status deployment/quantumtrade-frontend
```

## 📈 Performance Optimization

### Database Optimization

-   Use connection pooling
-   Implement database indexing
-   Optimize queries
-   Use read replicas for scaling

### Caching

Implement caching strategies:

```python
from fastapi import FastAPI
from fastapi.middleware.caching import CacheMiddleware

app = FastAPI()
app.add_middleware(CacheMiddleware, ttl=300)  # Cache for 5 minutes

@app.get("/api/market-data")
async def get_market_data():
    # This response will be cached
    return {"data": "market_data"}
```

### Load Balancing

Configure load balancing for high availability:

-   Use deployment platform's built-in load balancing
-   Configure health checks
-   Set up auto-scaling rules

## 🛠️ Troubleshooting

### Common Deployment Issues

#### Build Failures

```bash
# Check Docker build logs
docker build . --no-cache

# Debug failing tests
pytest -s -v tests/unit/test_failing.py
```

#### Deployment Issues

```bash
# Check container logs
docker logs quantumtrade-backend

# Verify environment variables
docker exec -it quantumtrade-backend env
```

#### Network Issues

```bash
# Test connectivity
curl -v $SUPABASE_URL

# Check DNS resolution
nslookup your-supabase-project.supabase.co
```

### Debugging Tips

#### Local Pipeline Testing

```bash
# Test GitHub Actions locally
act push -j test

# Run specific workflow
act pull_request -W .github/workflows/deploy.yml
```

#### Incremental Testing

```bash
# Test individual pipeline stages
# 1. Run tests locally
# 2. Build Docker images locally
# 3. Test deployment to staging
```

## 📋 Checklist

### Pre-Deployment

-   [ ] All tests passing
-   [ ] Code coverage above threshold
-   [ ] Security scans clean
-   [ ] Docker images built successfully
-   [ ] Environment variables configured

### Deployment

-   [ ] Health checks passing
-   [ ] Smoke tests successful
-   [ ] Monitoring alerts configured
-   [ ] Rollback plan documented

### Post-Deployment

-   [ ] Performance metrics stable
-   [ ] User acceptance testing
-   [ ] Documentation updated
-   [ ] Team notified of deployment

## 📚 Additional Resources

-   [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
-   [Render Deployment Documentation](https://render.com/docs)
-   [Railway Deployment Guide](https://docs.railway.app)
-   [Fly.io Deployment Documentation](https://fly.io/docs)
-   [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
-   [Vercel Deployment Documentation](https://vercel.com/docs)
