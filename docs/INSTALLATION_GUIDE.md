# QuantumTrade Installation Guide

## 📋 Prerequisites

Before installing QuantumTrade, ensure you have the following installed:

-   **Python 3.11+**
-   **Node.js 18+**
-   **Docker and Docker Compose**
-   **Git**
-   **Supabase account** (optional, for cloud features)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quantumtrade
```

### 2. Configure Environment Variables

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Supabase Configuration (optional)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quantumtrade

# Application Settings
SECRET_KEY=your_secret_key
DEBUG=True
PORT=8000

# AI/ML Settings
MODEL_PATH=./models

# Backtesting Settings
BACKTEST_DATA_PATH=./data
```

### 3. Install Dependencies

#### Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Set Up the Database

#### Using Docker (Recommended)

```bash
docker-compose up -d db
```

#### Initialize Database Schema

```bash
cd backend
python src/scripts/init_db.py
```

#### Seed Initial Data

```bash
python src/scripts/seed_data.py
```

### 5. Run the Application

#### Run Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Run Frontend

```bash
cd frontend
npm run dev
```

#### Run with Docker Compose (Alternative)

```bash
docker-compose up --build
```

## 🐳 Docker Installation

### Build Docker Images

```bash
docker-compose build
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Access Services

-   **Frontend**: http://localhost:5173
-   **Backend API**: http://localhost:8000
-   **Database**: postgresql://postgres:postgres@localhost:5432/quantumtrade

## ☁️ Supabase Setup (Optional)

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create an account
2. Create a new project
3. Note down your project URL and API keys

### 2. Configure Supabase Credentials

Update your `.env` file with Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_JWT_SECRET=your_jwt_secret
```

### 3. Run Supabase Sync

```bash
cd backend
python src/scripts/sync_supabase.py
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Run Specific Tests

```bash
# Run a specific test file
pytest tests/test_agents.py

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## 🛠️ Development Setup

### Install Development Tools

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Install linting tools
pip install black ruff
npm install -g eslint prettier
```

### Code Formatting

```bash
# Format Python code
black .

# Format JavaScript/JSX code
npm run format

# Lint Python code
ruff check .

# Lint JavaScript/JSX code
npm run lint
```

## 🔧 Troubleshooting

### Common Issues

#### Port Conflicts

If you encounter port conflicts:

1. Check which ports are in use:

    ```bash
    netstat -an | grep LISTEN
    ```

2. Change the port in your `.env` file:
    ```env
    PORT=8001
    ```

#### Database Connection Issues

If you have database connection issues:

1. Ensure the database container is running:

    ```bash
    docker-compose ps
    ```

2. Check database logs:

    ```bash
    docker-compose logs db
    ```

3. Verify database credentials in `.env` file

#### Dependency Installation Issues

If you encounter dependency installation issues:

1. Update pip:

    ```bash
    pip install --upgrade pip
    ```

2. Install dependencies with verbose output:
    ```bash
    pip install -r requirements.txt -v
    ```

### Clean Installation

To perform a clean installation:

1. Remove existing containers and volumes:

    ```bash
    docker-compose down -v
    ```

2. Remove virtual environments:

    ```bash
    rm -rf backend/venv
    rm -rf frontend/node_modules
    ```

3. Start fresh installation following the steps above

## 📚 Additional Resources

-   [Project Overview](PROJECT_OVERVIEW.md)
-   [Supabase Setup Guide](SUPABASE_SETUP.md)
-   [Backtesting Engine Documentation](BACKTESTING_ENGINE.md)
-   [Agent Design Documentation](AGENT_DESIGN.md)
-   [Deployment Guide](DEPLOYMENT_GUIDE.md)
-   [CI/CD Pipeline Documentation](CI_CD_PIPELINE.md)
