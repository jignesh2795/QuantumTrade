# Deployment Guide

This document provides instructions for deploying the QuantumTrade system.

## Overview

QuantumTrade supports multiple deployment environments:

-   Local development (Docker Compose)
-   Staging environment
-   Production environment

## Prerequisites

### System Requirements

-   Docker 20.10+
-   Docker Compose 1.29+
-   4GB+ RAM
-   10GB+ free disk space

### Software Dependencies

-   Git
-   Bash shell (or equivalent)
-   Text editor

## Local Development Deployment

### 1. Clone Repository

```bash
git clone <repository-url>
cd quantumtrade
```

### 2. Environment Configuration

Copy and configure environment files:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services

```bash
docker-compose up --build
```

### 4. Access Services

-   Frontend: http://localhost:5173
-   Backend API: http://localhost:8000
-   Database: Internal to Docker network
-   Monitoring: Prometheus (9090), Grafana (3001)

## Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Application Deployment

```bash
# Clone repository
git clone <repository-url>
cd quantumtrade

# Configure production environment
cp .env.example .env
# Edit .env with production settings

# Build and start services
docker-compose -f docker-compose.prod.yml up -d
```

### 3. SSL Configuration

For production deployments, configure SSL using Let's Encrypt:

```bash
# Install Certbot
sudo apt install certbot -y

# Obtain SSL certificate
sudo certbot certonly --standalone -d yourdomain.com

# Configure Nginx with SSL
# (Update nginx configuration with certificate paths)
```

### 4. Monitoring Setup

```bash
# Access Grafana
http://yourdomain.com:3001

# Default credentials:
# Username: admin
# Password: admin

# Configure data sources:
# - Prometheus: http://prometheus:9090
```

## Environment Variables

### Required Variables

```bash
# Database configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Supabase configuration
SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# API configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security
JWT_SECRET=your-jwt-secret
```

### Optional Variables

```bash
# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/quantumtrade/backend.log

# Performance
WORKER_COUNT=4
MAX_CONNECTIONS=100

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

## Docker Configuration

### Development Configuration

```yaml
version: "3.8"
services:
    frontend:
        build:
            context: ./frontend
            dockerfile: Dockerfile.dev
        ports:
            - "5173:5173"
        volumes:
            - ./frontend:/app
        environment:
            - VITE_API_URL=http://localhost:8000

    backend:
        build:
            context: ./backend
            dockerfile: Dockerfile.dev
        ports:
            - "8000:8000"
        volumes:
            - ./backend:/app
        environment:
            - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

### Production Configuration

```yaml
version: "3.8"
services:
    frontend:
        build:
            context: ./frontend
            dockerfile: Dockerfile
        ports:
            - "80:80"
            - "443:443"
        environment:
            - VITE_API_URL=https://api.yourdomain.com

    backend:
        build:
            context: ./backend
            dockerfile: Dockerfile
        ports:
            - "8000:8000"
        environment:
            - DATABASE_URL=postgresql://user:password@db:5432/database
            - WORKER_COUNT=4
```

## Database Deployment

### Initial Setup

```bash
# Run database migrations
docker-compose exec backend python -m src.database.migrations

# Seed initial data
docker-compose exec backend python -m src.database.seed_data
```

### Backup and Restore

```bash
# Create backup
docker-compose exec db pg_dump -U postgres postgres > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres postgres < backup.sql
```

### Monitoring

```bash
# Check database health
docker-compose exec db pg_isready

# View database logs
docker-compose logs db
```

## Monitoring and Logging

### Prometheus Configuration

```yaml
# prometheus.yml
global:
    scrape_interval: 15s

scrape_configs:
    - job_name: "quantumtrade"
      static_configs:
          - targets: ["backend:8000"]
```

### Grafana Setup

1. Access Grafana at http://localhost:3001
2. Add Prometheus as data source
3. Import dashboards from `monitoring/grafana/dashboards/`

### Log Management

```bash
# View logs
docker-compose logs -f

# Export logs
docker-compose logs --since 1h > logs.txt
```

## Scaling Considerations

### Horizontal Scaling

```bash
# Scale backend workers
docker-compose up -d --scale backend=3

# Scale database (requires clustering setup)
docker-compose up -d --scale db=2
```

### Resource Allocation

```yaml
services:
    backend:
        deploy:
            resources:
                limits:
                    cpus: "0.5"
                    memory: 512M
                reservations:
                    cpus: "0.25"
                    memory: 256M
```

## Security Considerations

### Network Security

```yaml
# docker-compose.yml
services:
    backend:
        networks:
            - frontend
            - backend
        expose:
            - "8000"

networks:
    frontend:
        driver: bridge
    backend:
        driver: bridge
```

### Secret Management

```bash
# Use Docker secrets
echo "your-secret" | docker secret create db_password -

# Reference in compose file
services:
  backend:
    secrets:
      - db_password
```

## Backup and Disaster Recovery

### Automated Backups

```bash
# Daily backup script
#!/bin/bash
docker-compose exec db pg_dump -U postgres postgres > /backups/backup-$(date +%Y%m%d).sql

# Schedule with cron
0 2 * * * /path/to/backup-script.sh
```

### Recovery Process

```bash
# Stop services
docker-compose down

# Restore database
docker-compose up -d db
docker-compose exec -T db psql -U postgres postgres < backup.sql

# Start all services
docker-compose up -d
```

## Troubleshooting

### Common Issues

#### Service Won't Start

```bash
# Check service logs
docker-compose logs <service-name>

# Check service status
docker-compose ps

# Restart service
docker-compose restart <service-name>
```

#### Database Connection Issues

```bash
# Check database connectivity
docker-compose exec backend python -c "import psycopg2; print('Connected')"

# Check database logs
docker-compose logs db
```

#### Performance Issues

```bash
# Monitor resource usage
docker stats

# Check application logs
docker-compose logs backend

# Profile database queries
docker-compose exec db psql -U postgres -c "SELECT * FROM pg_stat_statements;"
```

### Health Checks

```bash
# Backend health check
curl http://localhost:8000/health

# Database health check
docker-compose exec db pg_isready

# Frontend health check
curl http://localhost:5173
```

## Maintenance

### Regular Tasks

```bash
# Update containers
docker-compose pull
docker-compose up -d

# Clean up unused resources
docker system prune -f

# Rotate logs
docker-compose exec backend logrotate /etc/logrotate.conf
```

### Monitoring Alerts

Configure alerts for:

-   High CPU usage
-   Low disk space
-   Database connection failures
-   API error rates
-   Trading performance anomalies

## Rollback Procedure

### Version Rollback

```bash
# Stop current services
docker-compose down

# Checkout previous version
git checkout v1.2.0

# Start services
docker-compose up -d
```

### Database Rollback

```bash
# Restore from backup
docker-compose exec -T db psql -U postgres postgres < backup.sql
```

## Performance Tuning

### Database Optimization

```sql
-- Add indexes
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_portfolio_user ON portfolio(user_id);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM trades WHERE user_id = 'user123';
```

### Application Tuning

```bash
# Adjust worker count based on CPU cores
WORKER_COUNT=$(nproc)

# Optimize memory usage
PYTHON_MAX_MEMORY=1G
```

This deployment guide ensures QuantumTrade can be successfully deployed and maintained across different environments.
