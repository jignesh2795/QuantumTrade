# Setup Guide

This document provides detailed instructions for setting up the QuantumTrade platform.

## Prerequisites

### System Requirements

-   Operating System: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
-   RAM: 8GB minimum (16GB recommended)
-   Disk Space: 20GB free space
-   Docker: Version 20.10 or higher
-   Docker Compose: Version 1.29 or higher

### Software Dependencies

-   Git (latest version)
-   Python 3.11 (for local development)
-   Node.js 18 (for frontend development)
-   Text Editor (VS Code recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quantumtrade
```

### 2. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quantumtrade
SUPABASE_URL=postgresql://postgres:postgres@localhost:5432/quantumtrade
SUPABASE_KEY=your-supabase-key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security
JWT_SECRET=your-jwt-secret-key
```

### 3. Docker Setup

Ensure Docker and Docker Compose are installed and running:

```bash
# Check Docker version
docker --version
docker-compose --version

# Start Docker daemon (if not already running)
# On Windows/Mac: Start Docker Desktop
# On Linux: sudo systemctl start docker
```

### 4. Build and Start Services

```bash
# Build and start all services
docker-compose up --build

# For development with live reloading
docker-compose -f docker-compose.dev.yml up --build
```

### 5. Initial Database Setup

The database will be automatically initialized on first run. If you need to reinitialize:

```bash
# Stop services
docker-compose down

# Remove database volume (WARNING: This will delete all data)
docker volume rm quantumtrade_postgres_data

# Start services again
docker-compose up
```

## Development Setup

### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python src/main.py
```

### Frontend Development

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Configuration Files

### Docker Compose Files

-   `docker-compose.yml`: Production configuration
-   `docker-compose.dev.yml`: Development configuration with live reloading
-   `docker-compose.prod.yml`: Production configuration with SSL

### Environment Files

-   `.env`: Main environment configuration
-   `.env.example`: Template for environment variables
-   `.env.development`: Development-specific variables
-   `.env.production`: Production-specific variables

## Service Access

### After Successful Setup

-   **Frontend**: http://localhost:5173
-   **Backend API**: http://localhost:8000
-   **API Documentation**: http://localhost:8000/docs
-   **Database**: Internal Docker network (port 5432)
-   **Monitoring**:
    -   Prometheus: http://localhost:9090
    -   Grafana: http://localhost:3001

## Data Initialization

### Sample Data

The system includes sample data for testing:

-   BTC-USD historical data
-   Sample portfolio positions
-   Example trading strategies

### Custom Data

To use your own data:

1. Place CSV files in the `data/` directory
2. Update the data loader configuration
3. Restart the services

## Testing

### Run Backend Tests

```bash
cd backend
pytest tests/
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

### Integration Tests

```bash
# Run integration tests
docker-compose -f docker-compose.test.yml up
```

## Common Setup Issues

### Port Conflicts

If you encounter port conflicts:

1. Check which services are using the ports:
    ```bash
    netstat -an | grep :8000
    netstat -an | grep :5173
    ```
2. Update ports in `docker-compose.yml`:
    ```yaml
    ports:
        - "8001:8000" # Change host port to 8001
    ```

### Docker Permission Issues

On Linux, if you encounter permission issues:

```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
```

### Database Connection Issues

If the backend cannot connect to the database:

1. Check database service status:
    ```bash
    docker-compose ps
    ```
2. Verify database logs:
    ```bash
    docker-compose logs supabase-db
    ```
3. Check environment variables in `.env` file

## Verification

### Check Service Health

```bash
# Check all services
docker-compose ps

# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# Check database connectivity
docker-compose exec supabase-db pg_isready
```

### Verify Data Initialization

```bash
# Check if tables were created
docker-compose exec supabase-db psql -U postgres -c "\dt"

# Check sample data
docker-compose exec supabase-db psql -U postgres -c "SELECT COUNT(*) FROM trades;"
```

## Next Steps

### Explore the Platform

1. Visit http://localhost:5173 to access the frontend
2. Navigate to http://localhost:8000/docs for API documentation
3. Try executing sample trades through the interface

### Customize Configuration

1. Modify strategy parameters in the frontend
2. Adjust risk management settings
3. Configure monitoring alerts

### Add Your Own Data

1. Import your market data
2. Configure custom trading strategies
3. Set up automated data feeds

## Advanced Configuration

### SSL Setup

For production deployments with SSL:

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Update `docker-compose.prod.yml` with certificate paths
3. Configure Nginx for SSL termination

### Performance Tuning

```bash
# Adjust Docker resource allocation
# In Docker Desktop: Settings > Resources

# Optimize database performance
docker-compose exec supabase-db psql -U postgres -c "ANALYZE;"
```

### Backup Configuration

```bash
# Set up automated backups
# Add to crontab:
0 2 * * * /path/to/backup-script.sh
```

## Support

If you encounter issues during setup:

1. Check the troubleshooting guide
2. Review Docker logs: `docker-compose logs`
3. Verify all prerequisites are met
4. Contact support or open a GitHub issue

This setup guide should help you successfully install and configure the QuantumTrade platform for development or production use.
