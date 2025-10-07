# CI/CD Pipeline

## 🎯 Goals

The CI/CD pipeline automates testing, building, and deployment of the QuantumTrade platform to ensure code quality, security, and reliable delivery to production environments.

### Continuous Integration

-   Run tests on PRs and pushes
-   Build Docker images
-   Perform security scanning
-   Validate code quality

### Continuous Deployment

-   Deploy images to registry
-   Deploy to cloud platforms on push to `main`
-   Automate training and model deployment
-   Enable rollback capabilities

## 🔄 Workflows

### CI Workflow (`.github/workflows/ci.yml`)

Triggered on:

-   Pull requests to `develop` and `main` branches
-   Pushes to `develop` and `main` branches

Steps:

1. Checkout repository
2. Set up Python and Node.js environments
3. Install backend dependencies
4. Install frontend dependencies
5. Run backend tests
6. Run frontend tests
7. Build backend Docker image
8. Build frontend Docker image
9. Scan for security vulnerabilities
10. Validate code quality

### CD Workflow (`.github/workflows/cd.yml`)

Triggered on:

-   Pushes to `main` branch

Steps:

1. Checkout repository
2. Set up environments
3. Run extended test suite
4. Build production Docker images
5. Push images to container registry
6. Deploy to production environment
7. Run smoke tests
8. Notify team of deployment

### Scheduled Training (`.github/workflows/train.yml`)

Triggered:

-   Daily at 2 AM UTC

Steps:

1. Checkout repository
2. Set up Python environment
3. Install dependencies
4. Fetch training data
5. Train models
6. Validate model performance
7. Store model artifacts
8. Update production models if improved

## 🔐 Secrets Management

### Required Secrets

Configure the following secrets in your GitHub repository settings:

```env
# Docker Registry
DOCKERHUB_USERNAME=your_dockerhub_username
DOCKERHUB_PASSWORD=your_dockerhub_password
# or for GitHub Container Registry
GHCR_TOKEN=your_github_token

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Model Registry
MODEL_REGISTRY_KEY=your_model_registry_key

# Deployment
DEPLOYMENT_TOKEN=your_deployment_token
DEPLOYMENT_URL=your_deployment_url
```

## 🧪 Testing Pipeline

### Backend Testing

#### Unit Tests

```bash
# Run unit tests with coverage
cd backend
pytest tests/unit/ --cov=src --cov-report=xml

# Test specific modules
pytest tests/unit/test_agents.py
pytest tests/unit/test_strategy_agent.py::TestStrategyAgent::test_generate_signal
```

#### Integration Tests

```bash
# Run integration tests
cd backend
pytest tests/integration/

# Test database integration
pytest tests/integration/test_database.py
pytest tests/integration/test_supabase_integration.py
```

#### End-to-End Tests

```bash
# Run end-to-end tests
cd backend
pytest tests/e2e/

# Test API endpoints
pytest tests/e2e/test_api_endpoints.py
```

### Frontend Testing

#### Unit Tests

```bash
# Run frontend unit tests
cd frontend
npm test -- --coverage

# Test specific components
npm test src/components/TradingDashboard.test.js
```

#### Integration Tests

```bash
# Run frontend integration tests
cd frontend
npm run test:integration
```

#### End-to-End Tests

```bash
# Run frontend E2E tests
cd frontend
npm run test:e2e

# Run Cypress tests
npx cypress run
```

### Security Scanning

#### Dependency Scanning

```bash
# Scan Python dependencies
cd backend
safety check

# Scan Node.js dependencies
cd frontend
npm audit
```

#### Code Scanning

```bash
# Scan Python code for vulnerabilities
cd backend
bandit -r src/

# Scan JavaScript code for vulnerabilities
cd frontend
npm run lint:security
```

## 🐳 Docker Build Process

### Multi-Stage Builds

#### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Build Optimization

#### Caching Strategies

```dockerfile
# Cache dependencies separately from source code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
```

#### Layer Optimization

```dockerfile
# Combine related commands to reduce layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*
```

## ☁️ Deployment Process

### Supabase Deployment

#### Database Migrations

```bash
# Apply database migrations
supabase migration up

# Create new migration
supabase migration new add_trades_table
```

#### Function Deployment

```bash
# Deploy Supabase functions
supabase functions deploy --project-ref your-project-ref

# Deploy specific function
supabase functions deploy trading-webhook --project-ref your-project-ref
```

### Frontend Deployment (Vercel)

#### Vercel Configuration

```json
// frontend/vercel.json
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

#### Deployment Commands

```bash
# Deploy to Vercel
cd frontend
vercel --prod

# Deploy preview
vercel
```

### Backend Deployment

#### Container Deployment

```bash
# Deploy backend container
docker run -d \
  --name quantumtrade-backend \
  -p 8000:8000 \
  -e SUPABASE_URL=$SUPABASE_URL \
  -e SUPABASE_KEY=$SUPABASE_KEY \
  ghcr.io/your-username/quantumtrade/backend:latest
```

#### Kubernetes Deployment (Optional)

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
    name: quantumtrade-backend
spec:
    replicas: 3
    selector:
        matchLabels:
            app: quantumtrade-backend
    template:
        metadata:
            labels:
                app: quantumtrade-backend
        spec:
            containers:
                - name: backend
                  image: ghcr.io/your-username/quantumtrade/backend:latest
                  ports:
                      - containerPort: 8000
                  env:
                      - name: SUPABASE_URL
                        valueFrom:
                            secretKeyRef:
                                name: supabase-config
                                key: url
                      - name: SUPABASE_KEY
                        valueFrom:
                            secretKeyRef:
                                name: supabase-config
                                key: key
```

## 📊 Monitoring and Observability

### Test Results Tracking

#### Code Coverage

```yaml
# Upload coverage reports
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
      file: ./backend/coverage.xml
      flags: backend
```

#### Performance Metrics

```bash
# Track test execution time
pytest --durations=10
```

### Deployment Verification

#### Health Checks

```bash
# Verify backend deployment
curl -f http://your-backend-url/health

# Verify frontend deployment
curl -f http://your-frontend-url/
```

#### Smoke Tests

```bash
# Run smoke tests after deployment
cd tests/smoke
pytest test_deployment.py
```

## 🔐 Security Pipeline

### Secret Management

#### GitHub Secrets

```bash
# Set GitHub secrets
gh secret set SUPABASE_URL --body="your-supabase-url"
gh secret set SUPABASE_KEY --body="your-supabase-key"
```

#### Environment Variables

```yaml
# Use secrets in workflows
env:
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
    SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
```

### Security Scanning

#### Static Analysis

```yaml
- name: Run security audit
  run: |
      cd backend
      bandit -r src/
      safety check
```

#### Container Scanning

```yaml
- name: Scan container for vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
      image-ref: ghcr.io/your-username/quantumtrade/backend:latest
      format: sarif
      output: trivy-results.sarif
```

## 🔄 Continuous Delivery

### Environment Promotion

#### Development → Staging → Production

```yaml
# Deploy to staging on develop branch
deploy-staging:
    if: github.ref == 'refs/heads/develop'
    # ... deployment steps

# Deploy to production on main branch
deploy-production:
    if: github.ref == 'refs/heads/main'
    # ... deployment steps
```

### Rollback Procedures

#### Automated Rollback

```yaml
- name: Check deployment health
  run: |
      if ! curl -f http://your-app/health; then
        echo "Deployment failed, rolling back..."
        # Rollback implementation
        exit 1
      fi
```

#### Manual Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/quantumtrade-backend
```

## 📈 Performance Optimization

### Pipeline Speed

#### Parallel Jobs

```yaml
# Run tests in parallel
test-backend:
    # ... backend tests

test-frontend:
    # ... frontend tests
# Both jobs run simultaneously
```

#### Caching

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
      path: |
          ~/.cache/pip
          node_modules
      key: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt', '**/package-lock.json') }}
```

### Resource Management

#### Resource Limits

```yaml
jobs:
    test:
        runs-on: ubuntu-latest
        container:
            image: python:3.11
            resources:
                limits:
                    cpu: 2
                    memory: 4Gi
```

## 🛠️ Customization

### Environment-Specific Configuration

#### Multiple Environments

```yaml
# Deploy to different environments
env:
    DEVELOPMENT:
        SUPABASE_URL: ${{ secrets.DEV_SUPABASE_URL }}
    STAGING:
        SUPABASE_URL: ${{ secrets.STAGING_SUPABASE_URL }}
    PRODUCTION:
        SUPABASE_URL: ${{ secrets.PROD_SUPABASE_URL }}
```

### Notification System

#### Slack Notifications

```yaml
- name: Notify on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
      status: ${{ job.status }}
      channel: "#ci-cd-alerts"
```

#### Email Notifications

```yaml
- name: Send email on deployment
  if: success()
  uses: dawidd6/action-send-mail@v1
  with:
      server_address: smtp.gmail.com
      server_port: 465
      username: ${{ secrets.MAIL_USERNAME }}
      password: ${{ secrets.MAIL_PASSWORD }}
      subject: QuantumTrade Deployment Success
      body: Deployment to production completed successfully
      to: team@quantumtrade.com
```

## 📚 Monitoring Dashboard

### GitHub Actions Dashboard

Track pipeline status:

-   Success rate
-   Average build time
-   Test coverage
-   Deployment frequency

### Performance Metrics

#### Build Times

```bash
# Track build performance
echo "Build completed in $(date -d @$((END_TIME - START_TIME)) -u +%H:%M:%S)"
```

#### Resource Usage

```yaml
- name: Monitor resource usage
  run: |
      echo "CPU usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)"
      echo "Memory usage: $(free | grep Mem | awk '{printf("%.2f%%", $3/$2 * 100.0)}')"
```

## 🔧 Troubleshooting

### Common Issues

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
act pull_request -W .github/workflows/ci_cd.yml
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

-   [GitHub Actions Documentation](https://docs.github.com/en/actions)
-   [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
-   [Supabase Deployment Guide](https://supabase.com/docs/guides/deployment)
-   [Vercel Deployment Documentation](https://vercel.com/docs)
