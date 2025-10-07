# QuantumTrade Development Guide

This guide provides comprehensive information for developers working on the QuantumTrade platform.

## Project Overview

QuantumTrade is an AI-driven trading platform built with modern technologies:

-   **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
-   **Frontend**: React, Vite, Chart.js
-   **Infrastructure**: Docker, Docker Compose, Prometheus, Grafana
-   **Database**: PostgreSQL with Supabase integration

## Development Environment Setup

### Prerequisites

-   Python 3.11+
-   Node.js 18+
-   Docker and Docker Compose
-   Git
-   VS Code (recommended IDE)

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd quantumtrade

# Set up backend development environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up frontend development environment
cd ../frontend
npm install

# Configure environment variables
cp ../.env.example ../.env
# Edit ../.env with your configuration
```

### Development Workflow

```bash
# Start backend in development mode
cd backend
python src/main.py

# Start frontend in development mode
cd frontend
npm run dev

# Or use Docker for containerized development
cd ..
docker-compose -f docker-compose.dev.yml up
```

## Backend Development

### Project Structure

```
backend/
├── src/
│   ├── agents/           # Trading agents
│   ├── api/              # API endpoints and routing
│   ├── config/           # Configuration management
│   ├── core/             # Core trading engine
│   ├── database/         # Database models and connections
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions
│   └── main.py          # Application entry point
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── Dockerfile           # Docker configuration
```

### Adding New API Endpoints

1. Create a new route file in `src/api/routes/`
2. Define your endpoints using FastAPI decorators
3. Register the router in `src/api/routes/__init__.py`
4. Add appropriate middleware and security

Example:

```python
# src/api/routes/example.py
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])

@router.get("/")
async def get_example():
    return {"message": "Hello, World!"}
```

### Creating Trading Agents

1. Create a new agent file in `src/agents/`
2. Inherit from base agent classes if applicable
3. Implement required methods
4. Register in `src/agents/__init__.py`

Example:

```python
# src/agents/example_agent.py
from typing import Dict, Any

class ExampleAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement agent logic
        return {"result": "processed"}
```

### Database Operations

1. Define models in `src/database/models.py`
2. Create CRUD operations in `src/database/repositories.py`
3. Use SQLAlchemy for database interactions
4. Handle transactions properly

Example:

```python
# src/database/repositories.py
from sqlalchemy.orm import Session
from .models import Trade

class TradeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_trade(self, trade_data: dict) -> Trade:
        trade = Trade(**trade_data)
        self.db.add(trade)
        self.db.commit()
        self.db.refresh(trade)
        return trade
```

## Frontend Development

### Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/            # Application pages
│   ├── services/         # API service integrations
│   ├── hooks/            # Custom React hooks
│   ├── context/          # React context providers
│   ├── features/         # Feature-specific modules
│   ├── utils/            # Frontend utilities
│   ├── App.jsx          # Main application component
│   └── main.jsx         # React entry point
├── public/               # Static assets
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite configuration
```

### Creating New Components

1. Create component file in `src/components/`
2. Use functional components with hooks
3. Implement proper TypeScript interfaces
4. Add CSS modules for styling

Example:

```jsx
// src/components/ExampleComponent.jsx
import React from "react";

const ExampleComponent = ({ message }) => {
    return (
        <div className="example-component">
            <h2>{message}</h2>
        </div>
    );
};

export default ExampleComponent;
```

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route in `src/App.jsx`
3. Implement page logic and UI
4. Connect to backend services

Example:

```jsx
// src/pages/ExamplePage.jsx
import React from "react";
import ExampleComponent from "../components/ExampleComponent";

const ExamplePage = () => {
    return (
        <div>
            <h1>Example Page</h1>
            <ExampleComponent message="Hello from example page" />
        </div>
    );
};

export default ExamplePage;
```

### API Integration

1. Create service files in `src/services/`
2. Use axios for HTTP requests
3. Handle errors appropriately
4. Implement caching where beneficial

Example:

```javascript
// src/services/exampleService.js
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const getExampleData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/example`);
        return response.data;
    } catch (error) {
        console.error("Error fetching example data:", error);
        throw error;
    }
};
```

## Testing

### Backend Testing

```bash
# Run all tests
cd backend
pytest

# Run specific test file
pytest tests/test_example.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests
pytest -m integration tests/
```

### Frontend Testing

```bash
# Run all tests
cd frontend
npm test

# Run tests in watch mode
npm run test:watch

# Run specific test file
npm test -- src/components/ExampleComponent.test.js

# Run integration tests
npm run test:integration
```

### Writing Tests

Backend example:

```python
# tests/test_example.py
import pytest
from src.agents.example_agent import ExampleAgent

def test_example_agent_process():
    agent = ExampleAgent({"param": "value"})
    result = agent.process({"input": "data"})
    assert result["result"] == "processed"
```

Frontend example:

```javascript
// src/components/ExampleComponent.test.js
import { render, screen } from "@testing-library/react";
import ExampleComponent from "./ExampleComponent";

test("renders message correctly", () => {
    render(<ExampleComponent message="Test Message" />);
    expect(screen.getByText("Test Message")).toBeInTheDocument();
});
```

## Code Quality and Standards

### Python Standards

-   Follow PEP 8 style guide
-   Use type hints where possible
-   Write docstrings for public functions
-   Keep functions small and focused

### JavaScript/React Standards

-   Use functional components with hooks
-   Follow React best practices
-   Use PropTypes or TypeScript for type checking
-   Keep components small and reusable

### Git Workflow

1. Create feature branches from `develop`
2. Write descriptive commit messages
3. Keep commits small and focused
4. Create pull requests for code review

Example commit message:

```
feat(trading): add Bollinger Bands strategy

Implement Bollinger Bands trading strategy with configurable parameters

- Add BollingerBandsStrategy class
- Implement signal generation logic
- Add configuration options
- Include unit tests

Closes #123
```

## Docker Development

### Development Containers

Use `docker-compose.dev.yml` for development:

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Rebuild specific service
docker-compose -f docker-compose.dev.yml build backend

# Access container shell
docker-compose -f docker-compose.dev.yml exec backend /bin/bash
```

### Debugging in Containers

```bash
# Check container logs
docker-compose logs backend

# Monitor resource usage
docker stats

# Execute commands in container
docker-compose exec backend python -c "print('Hello from container')"
```

## Database Development

### Schema Changes

1. Update models in `src/database/models.py`
2. Create migration scripts
3. Test changes locally
4. Apply to production carefully

### Data Seeding

```bash
# Run seed script
docker-compose exec backend python -m src.database.seed_data

# Custom seed data
docker-compose exec backend python -c "
from src.database.seed_data import seed_custom_data
seed_custom_data()
"
```

## Monitoring and Logging

### Adding Metrics

```python
# src/utils/metrics.py
from prometheus_client import Counter, Histogram

TRADE_COUNTER = Counter('trades_total', 'Total trades executed')
TRADE_LATENCY = Histogram('trade_latency_seconds', 'Trade execution latency')

def record_trade():
    TRADE_COUNTER.inc()
```

### Logging Best Practices

```python
# src/utils/logger.py
import logging

logger = logging.getLogger(__name__)

def log_trade_execution(trade_data):
    logger.info(f"Trade executed: {trade_data}", extra={
        "trade_id": trade_data.get("id"),
        "symbol": trade_data.get("symbol"),
        "amount": trade_data.get("amount")
    })
```

## Performance Optimization

### Backend Optimization

1. Use database indexing
2. Implement caching strategies
3. Optimize database queries
4. Use asynchronous processing where appropriate

### Frontend Optimization

1. Implement code splitting
2. Optimize bundle size
3. Use React.memo for components
4. Implement virtual scrolling for large lists

## Security Considerations

### Input Validation

```python
# src/api/routes/example.py
from pydantic import BaseModel, validator

class TradeRequest(BaseModel):
    symbol: str
    amount: float

    @validator('symbol')
    def validate_symbol(cls, v):
        if not v or len(v) > 20:
            raise ValueError('Invalid symbol')
        return v
```

### Authentication

```python
# src/api/middleware/auth.py
from fastapi import HTTPException, Depends
from src.utils.auth import verify_token

async def authenticate_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

## Deployment and CI/CD

### Local Testing

```bash
# Test production build
docker-compose -f docker-compose.prod.yml up --build

# Run integration tests
docker-compose -f docker-compose.test.yml up
```

### Environment-Specific Configuration

Use environment variables for configuration:

```python
# src/config/settings.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    JWT_SECRET = os.getenv("JWT_SECRET", "secret-key")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

## Troubleshooting Development Issues

### Common Development Problems

#### Import Errors

```bash
# Check Python path
python -c "import sys; print('\\n'.join(sys.path))"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Database Connection Issues

```bash
# Test database connection
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://user:pass@localhost:5432/db')
print('Connected successfully')
"

# Check database service
docker-compose exec db pg_isready
```

#### Frontend Build Failures

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Contributing Guidelines

### Code Review Process

1. Create pull request with clear description
2. Ensure all tests pass
3. Address all review comments
4. Squash commits before merge

### Documentation Updates

1. Update relevant documentation files
2. Add docstrings to new functions
3. Update API documentation
4. Include examples where helpful

### Testing Requirements

1. Write unit tests for new functionality
2. Update integration tests as needed
3. Ensure test coverage > 80%
4. Run all tests before submitting PR

This development guide provides the foundation for contributing to the QuantumTrade platform. For specific questions or issues, refer to the team leads or documentation maintainers.
