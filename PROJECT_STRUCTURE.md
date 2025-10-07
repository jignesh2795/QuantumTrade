# QuantumTrade Project Structure

```
quantumtrade/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
│   ├── README.md
│   ├── setup.md
│   ├── api.md
│   ├── architecture.md
│   ├── deployment.md
│   ├── troubleshooting.md
│   ├── stages/
│   │   ├── README.md
│   │   ├── stage1.md
│   │   ├── stage2.md
│   │   ├── stage3.md
│   │   ├── stage3_5.md
│   │   ├── stage4.md
│   │   ├── stage5.md
│   │   └── summary.md
│   └── ...
├── scripts/
│   ├── start.sh         # One-command root start
│   ├── setup.sh         # One-command root setup
│   └── cleanup.sh       # Safe Docker cleanup
├── frontend/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── features/
│       ├── components/
│       ├── hooks/
│       ├── context/
│       ├── services/
│       └── utils/
├── backend/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── requirements.txt
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── model_server.py
│   │   │   └── ...
│   │   ├── services/
│   │   ├── agents/
│   │   │   └── plugins/
│   │   ├── api/
│   │   │   ├── server.py
│   │   │   ├── routes/
│   │   │   └── middleware/
│   │   ├── database/
│   │   │   └── migrations/
│   │   ├── config/
│   │   │   ├── environments/
│   │   │   └── feature_flags.yaml
│   │   ├── sync/
│   │   │   ├── sync_service.py
│   │   │   ├── webhooks.py
│   │   │   └── mock_data_loader.py
│   │   └── utils/
│   ├── tests/
│   └── scripts/
│       ├── db_migrate.sh
├── docker/
│   ├── docker-compose.yml
│   └── .dockerignore
```

## Key Directories and Files

### Root Directory

-   `README.md` - Project overview and quick start guide
-   `.gitignore` - Git ignore patterns
-   `.env.example` - Environment variable templates

### Docs Directory

-   Comprehensive documentation for all development stages
-   Setup guides, API documentation, and troubleshooting guides
-   Stage-specific documentation for each development phase

### Scripts Directory

-   Utility scripts for starting, setting up, and cleaning the project
-   Cross-platform shell scripts for common operations

### Frontend Directory

-   React/Vite-based frontend application
-   Component architecture with features, hooks, and services
-   Docker configuration for containerized deployment

### Backend Directory

-   FastAPI-based backend API
-   Modular agent system for trading operations
-   Core modules for trading logic and services
-   Database models and migrations
-   Configuration files and utilities
-   Sync services for Supabase integration

### Docker Directory

-   Docker Compose configuration for multi-container deployment
-   Docker ignore patterns for efficient builds
