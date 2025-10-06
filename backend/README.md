# QuantumTrade Backend

Python backend for the QuantumTrade platform using FastAPI.

## Features

- FastAPI for REST API
- SQLAlchemy for database ORM
- Pydantic for data validation
- PostgreSQL database support
- AI agent framework

## Structure

```
src/
├── api/            # API routes and server
├── core/           # Core trading logic
├── agents/         # AI trading agents
├── services/       # Business logic services
├── database/       # Database models and connections
├── config/         # Configuration files
├── utils/          # Utility functions
└── main.py         # Application entry point
```

## Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

The backend will be available at http://localhost:8000