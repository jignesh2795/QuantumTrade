# Troubleshooting Guide

This document provides solutions to common issues encountered with the QuantumTrade system.

## Docker Issues

### Services Not Starting

**Problem**: Containers fail to start or exit immediately
**Solution**:

```bash
# Check container logs
docker-compose logs <service-name>

# Check resource allocation
docker stats

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Port Conflicts

**Problem**: "Port is already allocated" error
**Solution**:

```bash
# Check which process is using the port
netstat -an | grep :8000  # or :5173, :5432, etc.

# Kill the conflicting process
kill -9 <process-id>

# Or change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use different host port
```

### Docker Permission Denied

**Problem**: Permission denied when running Docker commands
**Solution**:

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER

# Log out and back in
# Or run with sudo temporarily
sudo docker-compose up
```

### Insufficient Resources

**Problem**: Containers crash due to memory/CPU limits
**Solution**:

```bash
# Increase Docker resource limits
# Docker Desktop: Settings > Resources > Memory/CPU

# Check current usage
docker stats

# Optimize container resources in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
      cpus: '0.5'
```

## Database Issues

### Connection Refused

**Problem**: Backend cannot connect to database
**Solution**:

```bash
# Check if database container is running
docker-compose ps

# Check database logs
docker-compose logs supabase-db

# Verify environment variables
echo $DATABASE_URL

# Test connection manually
docker-compose exec backend python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('Connected successfully')
"
```

### Database Initialization Failed

**Problem**: Tables not created or sample data missing
**Solution**:

```bash
# Check initialization logs
docker-compose logs supabase-db

# Manually initialize database
docker-compose exec supabase-db psql -U postgres -f /docker-entrypoint-initdb.d/init-db.sh

# Reset database (WARNING: Deletes all data)
docker-compose down -v
docker-compose up
```

### Slow Query Performance

**Problem**: Database queries are slow
**Solution**:

```bash
# Add database indexes
docker-compose exec supabase-db psql -U postgres -c "
CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
"

# Analyze query performance
docker-compose exec supabase-db psql -U postgres -c "
EXPLAIN ANALYZE SELECT * FROM trades WHERE user_id = 'user123';
"

# Optimize database configuration
# In docker-compose.yml:
environment:
  - POSTGRES_SHARED_BUFFERS=256MB
  - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
```

## Backend Issues

### Module Import Errors

**Problem**: "Module not found" or import errors
**Solution**:

```bash
# Check Python path
docker-compose exec backend python -c "import sys; print(sys.path)"

# Reinstall dependencies
docker-compose exec backend pip install -r requirements.txt --force-reinstall

# Check file structure
docker-compose exec backend ls -la src/
```

### Authentication Failures

**Problem**: JWT validation errors or authentication failures
**Solution**:

```bash
# Check JWT secret
echo $JWT_SECRET

# Verify token format
# Tokens should be in format: Bearer <token>

# Test Supabase connection
docker-compose exec backend python -c "
from src.database.supabase_client import test_supabase_connection
print(test_supabase_connection())
"
```

### API Endpoint Errors

**Problem**: 500 Internal Server errors on API calls
**Solution**:

```bash
# Check backend logs
docker-compose logs backend

# Test endpoint manually
curl -v http://localhost:8000/health

# Check for syntax errors
docker-compose exec backend python -m py_compile src/api/routes/*.py
```

## Frontend Issues

### Frontend Not Loading

**Problem**: Blank page or loading errors
**Solution**:

```bash
# Check frontend logs
docker-compose logs frontend

# Verify API connection
curl http://localhost:8000/health

# Check browser console for errors (F12)
```

### Build Failures

**Problem**: Frontend build fails during Docker build
**Solution**:

```bash
# Clean npm cache
docker-compose exec frontend npm cache clean --force

# Reinstall dependencies
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# Check for syntax errors
docker-compose exec frontend npm run build
```

### WebSocket Connection Issues

**Problem**: Real-time updates not working
**Solution**:

```bash
# Check WebSocket endpoint
curl -v http://localhost:8000/ws/

# Verify CORS settings
# Check backend/src/config/security.py

# Test with wscat
npm install -g wscat
wscat -c ws://localhost:8000/ws/trades
```

## Supabase Integration Issues

### Supabase Client Initialization

**Problem**: "Invalid URL" or client initialization errors
**Solution**:

```bash
# Check Supabase configuration
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Test connection
docker-compose exec backend python -c "
from src.database.supabase_client import test_supabase_connection
result = test_supabase_connection()
print(f'Connection test: {result}')
"
```

### CRUD Operation Failures

**Problem**: Database operations failing
**Solution**:

```bash
# Check table existence
docker-compose exec supabase-db psql -U postgres -c "\dt"

# Test basic operations
docker-compose exec backend python -c "
from src.database.supabase_crud import SupabaseCRUD
crud = SupabaseCRUD()
# Test a simple operation
result = crud.get_trades('test-user')
print(result)
"
```

## Monitoring Issues

### Prometheus Not Collecting Metrics

**Problem**: No metrics in Prometheus
**Solution**:

```bash
# Check metrics endpoint
curl http://localhost:8000/metrics

# Verify Prometheus configuration
docker-compose exec prometheus cat /etc/prometheus/prometheus.yml

# Check Prometheus logs
docker-compose logs prometheus
```

### Grafana Dashboard Issues

**Problem**: Dashboards not loading or showing data
**Solution**:

```bash
# Check Grafana status
curl http://localhost:3001/api/health

# Verify data source configuration
# Login to Grafana and check Configuration > Data Sources

# Check dashboard JSON
docker-compose exec grafana ls /var/lib/grafana/dashboards/
```

## Performance Issues

### High Memory Usage

**Problem**: System running out of memory
**Solution**:

```bash
# Check resource usage
docker stats

# Limit container resources
# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 512M

# Optimize application code
# Check for memory leaks in Python/JavaScript code
```

### Slow API Responses

**Problem**: API calls taking too long
**Solution**:

```bash
# Profile API endpoints
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Check database query performance
docker-compose exec supabase-db psql -U postgres -c "
SELECT query, calls, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 5;
"

# Add caching where appropriate
```

## Network Issues

### Cross-Origin Resource Sharing (CORS)

**Problem**: CORS errors in browser console
**Solution**:

```bash
# Check CORS configuration in backend
# backend/src/api/server.py

# Verify allowed origins
# backend/src/config/security.py

# Test CORS headers
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://localhost:8000/health
```

### DNS Resolution Issues

**Problem**: Cannot resolve service names in Docker network
**Solution**:

```bash
# Check Docker network
docker network ls

# Test service connectivity
docker-compose exec backend ping supabase-db

# Verify service names in docker-compose.yml
```

## Data Issues

### Missing Sample Data

**Problem**: No data in database tables
**Solution**:

```bash
# Check if seed script ran
docker-compose logs supabase-db

# Manually run seed script
docker-compose exec backend python -m src.database.seed_data

# Verify data exists
docker-compose exec supabase-db psql -U postgres -c "SELECT COUNT(*) FROM trades;"
```

### Data Consistency Issues

**Problem**: Inconsistent data between services
**Solution**:

```bash
# Check database constraints
docker-compose exec supabase-db psql -U postgres -c "\d trades"

# Verify foreign key relationships
docker-compose exec supabase-db psql -U postgres -c "
SELECT * FROM trades t
LEFT JOIN portfolio p ON t.user_id = p.user_id
WHERE p.user_id IS NULL;
"

# Run data validation scripts
```

## Development Environment Issues

### Hot Reloading Not Working

**Problem**: Code changes not reflected without restart
**Solution**:

```bash
# Use development Docker Compose file
docker-compose -f docker-compose.dev.yml up

# Check volume mounts in docker-compose.yml
volumes:
  - ./backend:/app  # Ensure this is present

# Verify file watching in application code
```

### IDE Integration Issues

**Problem**: IDE not recognizing project structure
**Solution**:

```bash
# Create IDE-specific configuration files
# .vscode/settings.json for VS Code
# .idea/ for PyCharm

# Install development dependencies
pip install -r requirements-dev.txt

# Configure Python interpreter path
```

## Security Issues

### Authentication Bypass

**Problem**: Unauthorized access to protected endpoints
**Solution**:

```bash
# Check authentication middleware
# backend/src/api/middleware/security_middleware.py

# Verify JWT validation
# backend/src/config/security.py

# Test protected endpoints
curl -H "Authorization: Bearer invalid-token" \
     http://localhost:8000/portfolio/list
```

### Security Vulnerabilities

**Problem**: Security scan detecting vulnerabilities
**Solution**:

```bash
# Update dependencies
docker-compose exec backend pip list --outdated

# Run security scans
docker-compose exec backend pip-audit

# Check for known vulnerabilities
npm audit fix
```

## Backup and Recovery Issues

### Backup Failure

**Problem**: Automated backups failing
**Solution**:

```bash
# Check backup script permissions
ls -la scripts/backup/*.sh

# Test backup manually
docker-compose exec supabase-db pg_dump -U postgres postgres > test_backup.sql

# Verify backup location
ls -la /backups/
```

### Restore Failure

**Problem**: Unable to restore from backup
**Solution**:

```bash
# Check backup file integrity
head -n 20 backup.sql

# Test restore in test environment
docker-compose exec -T supabase-db psql -U postgres postgres < backup.sql

# Verify restored data
docker-compose exec supabase-db psql -U postgres -c "SELECT COUNT(*) FROM trades;"
```

## Advanced Troubleshooting

### Debugging with Shell Access

```bash
# Access container shell
docker-compose exec backend /bin/bash

# Check environment variables
env | grep -i supabase

# Test network connectivity
ping supabase-db

# Check file permissions
ls -la /app/
```

### Logging and Monitoring

```bash
# Enable debug logging
# Set LOG_LEVEL=DEBUG in .env

# Tail specific service logs
docker-compose logs -f backend

# Export logs for analysis
docker-compose logs --since 1h > logs.txt
```

### Performance Profiling

```bash
# Profile Python code
docker-compose exec backend python -m cProfile -o profile.out src/main.py

# Analyze profile results
docker-compose exec backend python -c "
import pstats
stats = pstats.Stats('profile.out')
stats.sort_stats('cumulative').print_stats(10)
"
```

## Getting Help

If you're unable to resolve an issue:

1. **Check Logs**: `docker-compose logs <service>`
2. **Search Issues**: Check GitHub issues for similar problems
3. **Community Support**: Join the QuantumTrade community forum
4. **Professional Support**: Contact support@quantumtrade.com

Include the following information when seeking help:

-   Error messages and logs
-   System specifications (OS, Docker version, etc.)
-   Steps to reproduce the issue
-   What you've already tried

This troubleshooting guide covers the most common issues encountered with QuantumTrade and provides practical solutions to resolve them.
