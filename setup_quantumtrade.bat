@echo off
REM QuantumTrade Setup Script for Windows

echo 🚀 Starting full QuantumTrade setup...

REM -------------------------------
REM 1️⃣ Create folder structure
REM -------------------------------
echo 📁 Creating project folders...
mkdir docs >nul 2>&1
mkdir scripts >nul 2>&1
mkdir frontend\src\features >nul 2>&1
mkdir frontend\src\components >nul 2>&1
mkdir frontend\src\hooks >nul 2>&1
mkdir frontend\src\context >nul 2>&1
mkdir frontend\src\services >nul 2>&1
mkdir frontend\src\utils >nul 2>&1
mkdir frontend\public\assets >nul 2>&1
mkdir backend\src\core >nul 2>&1
mkdir backend\src\services >nul 2>&1
mkdir backend\src\agents\plugins >nul 2>&1
mkdir backend\src\api\routes >nul 2>&1
mkdir backend\src\api\middleware >nul 2>&1
mkdir backend\src\database\migrations >nul 2>&1
mkdir backend\src\config\environments >nul 2>&1
mkdir backend\src\utils >nul 2>&1
mkdir backend\tests >nul 2>&1
mkdir backend\scripts >nul 2>&1
mkdir docker >nul 2>&1
mkdir logs >nul 2>&1

REM -------------------------------
REM 2️⃣ Create placeholder files
REM -------------------------------
echo 📝 Creating placeholder files...

REM Root files
type nul > README.md
type nul > LICENSE
type nul > .gitignore
type nul > .env.example

REM Docs
type nul > docs\setup.md
type nul > docs\api.md
type nul > docs\architecture.md
type nul > docs\deployment.md
type nul > docs\troubleshooting.md
type nul > docs\git_workflow.md
type nul > docs\git_cheat_sheet.md

REM Scripts
type nul > scripts\start.sh
type nul > scripts\setup.sh
type nul > scripts\cleanup.sh

REM Frontend
type nul > frontend\Dockerfile
type nul > frontend\Dockerfile.dev
type nul > frontend\package.json
type nul > frontend\vite.config.js
type nul > frontend\src\main.jsx
type nul > frontend\src\App.jsx
type nul > frontend\public\index.html

REM Backend
type nul > backend\Dockerfile
type nul > backend\Dockerfile.dev
type nul > backend\requirements.txt
type nul > backend\src\__init__.py
type nul > backend\src\main.py
type nul > backend\src\core\__init__.py
type nul > backend\src\services\__init__.py
type nul > backend\src\agents\__init__.py
type nul > backend\src\agents\plugins\__init__.py
type nul > backend\src\api\server.py
type nul > backend\src\api\routes\__init__.py
type nul > backend\src\api\middleware\__init__.py
type nul > backend\src\database\migrations\__init__.py
type nul > backend\src\config\environments\development.yaml
type nul > backend\src\config\feature_flags.yaml
type nul > backend\src\utils\__init__.py
type nul > backend\tests\__init__.py
type nul > backend\scripts\db_migrate.sh

REM Docker folder
type nul > docker\docker-compose.yml
type nul > docker\.dockerignore

REM -------------------------------
REM 3️⃣ Backend dependencies
REM -------------------------------
echo 📦 Writing backend requirements...
echo fastapi==0.111.1 > backend\requirements.txt
echo uvicorn[standard]==0.23.2 >> backend\requirements.txt
echo sqlalchemy==2.0.22 >> backend\requirements.txt
echo psycopg2-binary==2.9.7 >> backend\requirements.txt
echo pydantic==2.6.0 >> backend\requirements.txt
echo python-dotenv==1.0.1 >> backend\requirements.txt
echo pytest==8.2.1 >> backend\requirements.txt
echo pytest-asyncio==0.22.0 >> backend\requirements.txt
echo requests==2.32.1 >> backend\requirements.txt
echo numpy==1.26.2 >> backend\requirements.txt
echo pandas==2.1.1 >> backend\requirements.txt
echo aiohttp==3.9.3 >> backend\requirements.txt

REM -------------------------------
REM 4️⃣ Frontend dependencies
REM -------------------------------
echo 📦 Writing frontend package.json...
echo { > frontend\package.json
echo   "name": "quantumtrade-frontend", >> frontend\package.json
echo   "version": "0.1.0", >> frontend\package.json
echo   "private": true, >> frontend\package.json
echo   "type": "module", >> frontend\package.json
echo   "scripts": { >> frontend\package.json
echo     "dev": "vite", >> frontend\package.json
echo     "build": "vite build", >> frontend\package.json
echo     "preview": "vite preview" >> frontend\package.json
echo   }, >> frontend\package.json
echo   "dependencies": { >> frontend\package.json
echo     "react": "^18.2.0", >> frontend\package.json
echo     "react-dom": "^18.2.0", >> frontend\package.json
echo     "axios": "^1.6.5", >> frontend\package.json
echo     "chart.js": "^4.4.0", >> frontend\package.json
echo     "react-chartjs-2": "^5.2.0", >> frontend\package.json
echo     "react-router-dom": "^6.17.0" >> frontend\package.json
echo   }, >> frontend\package.json
echo   "devDependencies": { >> frontend\package.json
echo     "@vitejs/plugin-react": "^4.1.0", >> frontend\package.json
echo     "vite": "^5.0.0" >> frontend\package.json
echo   } >> frontend\package.json
echo } >> frontend\package.json

REM -------------------------------
REM 5️⃣ Placeholder backend files
REM -------------------------------
echo ⚙️ Populating backend placeholder files...

echo from src.api.server import app > backend\src\main.py
echo. >> backend\src\main.py
echo if __name__ == "__main__": >> backend\src\main.py
echo     import uvicorn >> backend\src\main.py
echo     uvicorn.run^(app, host="0.0.0.0", port=8000, reload=True^) >> backend\src\main.py

echo from fastapi import FastAPI > backend\src\api\server.py
echo from fastapi.middleware.cors import CORSMiddleware >> backend\src\api\server.py
echo from src.api.routes import router >> backend\src\api\server.py
echo. >> backend\src\api\server.py
echo app = FastAPI^(title="QuantumTrade API"^) >> backend\src\api\server.py
echo. >> backend\src\api\server.py
echo # Add CORS middleware >> backend\src\api\server.py
echo app.add_middleware^( >> backend\src\api\server.py
echo     CORSMiddleware, >> backend\src\api\server.py
echo     allow_origins=["*"], >> backend\src\api\server.py
echo     allow_credentials=True, >> backend\src\api\server.py
echo     allow_methods=["*"], >> backend\src\api\server.py
echo     allow_headers=["*"], >> backend\src\api\server.py
echo ^) >> backend\src\api\server.py
echo. >> backend\src\api\server.py
echo @app.get^("/"^) >> backend\src\api\server.py
echo def root^(^): >> backend\src\api\server.py
echo     return {"message": "QuantumTrade API is running!"} >> backend\src\api\server.py
echo. >> backend\src\api\server.py
echo app.include_router^(router^) >> backend\src\api\server.py

echo from fastapi import APIRouter > backend\src\api\routes\__init__.py
echo from src.agents.strategy_agent import StrategyAgent >> backend\src\api\routes\__init__.py
echo from src.agents.data_agent import DataAgent >> backend\src\api\routes\__init__.py
echo from src.agents.risk_agent import RiskAgent >> backend\src\api\routes\__init__.py
echo from src.agents.portfolio import PortfolioAgent >> backend\src\api\routes\__init__.py
echo from src.agents.execution_agent import ExecutionAgent >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo router = APIRouter^(^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo portfolio = PortfolioAgent^(^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/health"^) >> backend\src\api\routes\__init__.py
echo def health_check^(^): >> backend\src\api\routes\__init__.py
echo     return {"status": "ok"} >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/agents"^) >> backend\src\api\routes\__init__.py
echo def list_agents^(^): >> backend\src\api\routes\__init__.py
echo     return {"agents": ["data_agent", "strategy_agent", "risk_agent", "portfolio", "execution_agent"]} >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/strategy/signal"^) >> backend\src\api\routes\__init__.py
echo def strategy_signal^(symbol: str = "BTC-USD"^): >> backend\src\api\routes\__init__.py
echo     agent = StrategyAgent^(symbol^) >> backend\src\api\routes\__init__.py
echo     return agent.generate_signal^(^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/data/price"^) >> backend\src\api\routes\__init__.py
echo def get_price^(symbol: str = "BTC-USD"^): >> backend\src\api\routes\__init__.py
echo     agent = DataAgent^(^) >> backend\src\api\routes\__init__.py
echo     return agent.get_price^(symbol^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.post^("/portfolio/add"^) >> backend\src\api\routes\__init__.py
echo def add_position^(symbol: str, size: float, price: float^): >> backend\src\api\routes\__init__.py
echo     return portfolio.add_position^(symbol, size, price^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/portfolio/list"^) >> backend\src\api\routes\__init__.py
echo def list_positions^(^): >> backend\src\api\routes\__init__.py
echo     return portfolio.list_positions^(^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.get^("/risk/assess"^) >> backend\src\api\routes\__init__.py
echo def assess_risk^(position_size: float = 1000, account_balance: float = 10000^): >> backend\src\api\routes\__init__.py
echo     agent = RiskAgent^(^) >> backend\src\api\routes\__init__.py
echo     return agent.assess_risk^(position_size, account_balance^) >> backend\src\api\routes\__init__.py
echo. >> backend\src\api\routes\__init__.py
echo @router.post^("/execute/trade"^) >> backend\src\api\routes\__init__.py
echo def execute_trade^(symbol: str, action: str, size: float^): >> backend\src\api\routes\__init__.py
echo     agent = ExecutionAgent^(^) >> backend\src\api\routes\__init__.py
echo     return agent.execute_trade^(symbol, action, size^) >> backend\src\api\routes\__init__.py

REM -------------------------------
REM 6️⃣ Placeholder frontend files
REM -------------------------------
echo ⚙️ Populating frontend placeholder files...

echo import React from "react"; > frontend\src\main.jsx
echo import ReactDOM from "react-dom/client"; >> frontend\src\main.jsx
echo import App from "./App"; >> frontend\src\main.jsx
echo. >> frontend\src\main.jsx
echo ReactDOM.createRoot^(document.getElementById^("root"^)^).render^( >> frontend\src\main.jsx
echo   ^<React.StrictMode^> >> frontend\src\main.jsx
echo     ^<App /^> >> frontend\src\main.jsx
echo   ^</React.StrictMode^> >> frontend\src\main.jsx
echo ^); >> frontend\src\main.jsx

echo import React from "react"; > frontend\src\App.jsx
echo import Signal from "./features/Signal"; >> frontend\src\App.jsx
echo import Portfolio from "./features/Portfolio"; >> frontend\src\App.jsx
echo import Risk from "./features/Risk"; >> frontend\src\App.jsx
echo. >> frontend\src\App.jsx
echo function App^(^) { >> frontend\src\App.jsx
echo   return ^( >> frontend\src\App.jsx
echo     ^<div style={{ padding: "2rem" }}^> >> frontend\src\App.jsx
echo       ^<h1^>QuantumTrade Frontend^</h1^> >> frontend\src\App.jsx
echo       ^<p^>Your app is running! Connect to the backend API at ^<code^>/api^</code^>.^</p^> >> frontend\src\App.jsx
echo       ^<Signal /^> >> frontend\src\App.jsx
echo       ^<Portfolio /^> >> frontend\src\App.jsx
echo       ^<Risk /^> >> frontend\src\App.jsx
echo     ^</div^> >> frontend\src\App.jsx
echo   ^); >> frontend\src\App.jsx
echo } >> frontend\src\App.jsx
echo. >> frontend\src\App.jsx
echo export default App; >> frontend\src\App.jsx

echo ^<!DOCTYPE html^> > frontend\public\index.html
echo ^<html lang="en"^> >> frontend\public\index.html
echo   ^<head^> >> frontend\public\index.html
echo     ^<meta charset="UTF-8" /^> >> frontend\public\index.html
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0" /^> >> frontend\public\index.html
echo     ^<title^>QuantumTrade^</title^> >> frontend\public\index.html
echo   ^</head^> >> frontend\public\index.html
echo   ^<body^> >> frontend\public\index.html
echo     ^<div id="root"^>^</div^> >> frontend\public\index.html
echo     ^<script type="module" src="/src/main.jsx"^>^</script^> >> frontend\public\index.html
echo   ^</body^> >> frontend\public\index.html
echo ^</html^> >> frontend\public\index.html

REM -------------------------------
REM 7️⃣ Scripts
REM -------------------------------
echo ⚙️ Populating scripts...

echo #!/bin/bash > scripts\setup.sh
echo # Install dependencies >> scripts\setup.sh
echo set -e >> scripts\setup.sh
echo echo "⚙️ Setting up QuantumTrade environment from root..." >> scripts\setup.sh
echo. >> scripts\setup.sh
echo # Backend >> scripts\setup.sh
echo cd backend >> scripts\setup.sh
echo python3 -m venv venv ^|^| echo "Venv exists" >> scripts\setup.sh
echo source venv/bin/activate >> scripts\setup.sh
echo pip install -r requirements.txt >> scripts\setup.sh
echo echo "✅ Backend dependencies installed" >> scripts\setup.sh
echo cd .. >> scripts\setup.sh
echo. >> scripts\setup.sh
echo # Frontend >> scripts\setup.sh
echo cd frontend >> scripts\setup.sh
echo npm install >> scripts\setup.sh
echo echo "✅ Frontend dependencies installed" >> scripts\setup.sh
echo cd .. >> scripts\setup.sh
echo. >> scripts\setup.sh
echo echo "✅ Setup complete! Run ./scripts/start.sh to start the application" >> scripts\setup.sh
echo echo "Or use Docker: docker-compose -f docker/docker-compose.yml up --build" >> scripts\setup.sh

echo #!/bin/bash > scripts\start.sh
echo # Start app ^(local or Docker^) >> scripts\start.sh
echo set -e >> scripts\start.sh
echo echo "🚀 Starting QuantumTrade from root..." >> scripts\start.sh
echo. >> scripts\start.sh
echo if [ -f .env ]; then >> scripts\start.sh
echo     export $^(grep -v '^^#' .env ^| xargs^) >> scripts\start.sh
echo fi >> scripts\start.sh
echo. >> scripts\start.sh
echo if command -v docker-compose ^&^> /dev/null; then >> scripts\start.sh
echo     echo "🐳 Starting with Docker Compose..." >> scripts\start.sh
echo     docker-compose -f docker/docker-compose.yml up --build >> scripts\start.sh
echo else >> scripts\start.sh
echo     echo "⚙️ Starting locally..." >> scripts\start.sh
echo. >> scripts\start.sh
echo     # Start backend >> scripts\start.sh
echo     cd backend >> scripts\start.sh
echo     if [ -d "venv" ]; then >> scripts\start.sh
echo         source venv/bin/activate >> scripts\start.sh
echo         echo "✅ Backend virtual environment activated" >> scripts\start.sh
echo     else >> scripts\start.sh
echo         echo "⚠️ Backend virtual environment not found. Run ./scripts/setup.sh first" >> scripts\start.sh
echo         exit 1 >> scripts\start.sh
echo     fi >> scripts\start.sh
echo. >> scripts\start.sh
echo     echo "🚀 Starting backend server on http://localhost:8000" >> scripts\start.sh
echo     uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload ^& >> scripts\start.sh
echo     cd .. >> scripts\start.sh
echo. >> scripts\start.sh
echo     # Start frontend >> scripts\start.sh
echo     cd frontend >> scripts\start.sh
echo     echo "🚀 Starting frontend on http://localhost:5173" >> scripts\start.sh
echo     npm run dev ^& >> scripts\start.sh
echo     cd .. >> scripts\start.sh
echo. >> scripts\start.sh
echo     echo "✅ QuantumTrade running locally!" >> scripts\start.sh
echo     echo "Frontend: http://localhost:5173" >> scripts\start.sh
echo     echo "Backend API: http://localhost:8000" >> scripts\start.sh
echo     echo "Press Ctrl+C to stop" >> scripts\start.sh
echo. >> scripts\start.sh
echo     # Wait for background processes >> scripts\start.sh
echo     wait >> scripts\start.sh
echo fi >> scripts\start.sh

echo #!/bin/bash > scripts\cleanup.sh
echo # Docker cleanup >> scripts\cleanup.sh
echo echo "🧹 Cleaning up Docker containers, images, volumes..." >> scripts\cleanup.sh
echo docker container prune -f >> scripts\cleanup.sh
echo docker image prune -f >> scripts\cleanup.sh
echo docker volume prune -f >> scripts\cleanup.sh
echo docker network prune -f >> scripts\cleanup.sh
echo docker builder prune -a --filter "until=72h" -f >> scripts\cleanup.sh
echo echo "✅ Cleanup complete!" >> scripts\cleanup.sh

REM -------------------------------
REM 8️⃣ Git Workflow Documentation
REM -------------------------------
echo 📝 Creating Git workflow documentation...
(
echo # QuantumTrade Git Workflow
echo.
echo This document describes the Git branching strategy and workflow for the QuantumTrade project.
echo.
echo ## 1️⃣ Branch Structure
echo.
echo - **main** → Production-ready, stable code
echo - **develop** → Integration branch, contains latest tested features
echo - **feature/^<name^>** → New feature development
echo - **bugfix/^<name^>** → Quick bug fixes
echo - **release/^<version^>** → Optional pre-release branch
echo.
echo ## 2️⃣ Standard Workflow
echo.
echo ### Start a new feature
echo.
echo ^```bash
echo git checkout develop
echo git pull origin develop
echo git checkout -b feature/add-new-agent
echo ^```
echo.
echo ### Work on the feature
echo.
echo Add/modify code, agents, API routes, frontend components
echo.
echo Stage and commit changes frequently
echo.
echo ^```bash
echo git add .
echo git commit -m "Add ^<short description^>: ^<details if needed^>"
echo ^```
echo.
echo Example:
echo.
echo ^```bash
echo git commit -m "Add RiskAgent and risk assessment API route"
echo ^```
echo.
echo ### Push feature branch to remote
echo.
echo ^```bash
echo git push origin feature/add-new-agent
echo ^```
echo.
echo ### Create a Pull Request ^(PR^)
echo.
echo - Target branch: develop
echo - Include description and changes
echo.
echo ### Code Review ^& Merge
echo.
echo After approval, merge PR into develop
echo.
echo Pull latest changes:
echo.
echo ^```bash
echo git checkout develop
echo git pull origin develop
echo ^```
echo.
echo ### Release / Production
echo.
echo ^```bash
echo git checkout main
echo git merge develop
echo git push origin main
echo git tag -a v0.2.0 -m "Release version 0.2.0"
echo git push origin v0.2.0
echo ^```
echo.
echo ## 3️⃣ Hotfixes
echo.
echo ### Start from main:
echo.
echo ^```bash
echo git checkout main
echo git pull origin main
echo git checkout -b bugfix/fix-api-error
echo ^```
echo.
echo ### Fix the bug, commit, push:
echo.
echo ^```bash
echo git add .
echo git commit -m "Fix: corrected API endpoint error"
echo git push origin bugfix/fix-api-error
echo ^```
echo.
echo ### Merge into main and develop:
echo.
echo ^```bash
echo git checkout main
echo git merge bugfix/fix-api-error
echo git push origin main
echo.
echo git checkout develop
echo git merge bugfix/fix-api-error
echo git push origin develop
echo ^```
echo.
echo ## 4️⃣ Tips for a clean repo
echo.
echo - Commit small, logical units
echo - Keep main always deployable
echo - Use develop for integration/testing
echo - Tag every release version
echo - Regularly clean up old branches:
echo.
echo ^```bash
echo git branch -d feature/old-feature
echo git push origin --delete feature/old-feature
echo ^```
) > docs\git_workflow.md

REM -------------------------------
REM 9️⃣ Git Cheat Sheet
REM -------------------------------
echo 📝 Creating Git cheat sheet...
(
echo # QuantumTrade Git Cheat Sheet
echo.
echo Quick reference for common Git operations in the QuantumTrade project.
echo.
echo ## 1️⃣ Initial Setup
echo.
echo ^```bash
echo # Initialize repo ^(already done if setup script ran^)
echo git init
echo.
echo # Add remote origin
echo git remote add origin ^<repo-url^>
echo.
echo # Pull latest develop/main
echo git checkout develop
echo git pull origin develop
echo ^```
echo.
echo ## 2️⃣ Creating a New Feature
echo.
echo ^```bash
echo # Start feature branch from develop
echo git checkout develop
echo git pull origin develop
echo git checkout -b feature/^<feature-name^>
echo.
echo # Work on feature
echo # ...
echo.
echo # Stage ^& commit
echo git add .
echo git commit -m "Feature: ^<short description^>"
echo.
echo # Push feature branch
echo git push origin feature/^<feature-name^>
echo ^```
echo.
echo ## 3️⃣ Creating a Hotfix / Bugfix
echo.
echo ^```bash
echo # Start hotfix from main
echo git checkout main
echo git pull origin main
echo git checkout -b bugfix/^<bug-name^>
echo.
echo # Fix the bug
echo # ...
echo.
echo # Stage ^& commit
echo git add .
echo git commit -m "Fix: ^<short description^>"
echo.
echo # Push bugfix branch
echo git push origin bugfix/^<bug-name^>
echo ^```
echo.
echo ## 4️⃣ Pull Request / Merge
echo.
echo ^```bash
echo # Merge feature/bugfix into develop
echo git checkout develop
echo git pull origin develop
echo git merge feature/^<feature-name^>   # or bugfix/^<bug-name^>
echo git push origin develop
echo.
echo # Merge develop into main for release
echo git checkout main
echo git merge develop
echo git push origin main
echo ^```
echo.
echo ## 5️⃣ Tagging a Release
echo.
echo ^```bash
echo git checkout main
echo git pull origin main
echo.
echo # Tag release
echo git tag -a v^<version^> -m "Release v^<version^>"
echo git push origin v^<version^>
echo ^```
echo.
echo Example:
echo.
echo ^```bash
echo git tag -a v0.2.0 -m "Release v0.2.0"
echo git push origin v0.2.0
echo ^```
echo.
echo ## 6️⃣ Updating Branches
echo.
echo ^```bash
echo # Update your branch with latest develop
echo git checkout feature/^<feature-name^>
echo git pull origin develop
echo git merge develop
echo ^```
echo.
echo ## 7️⃣ Cleaning Up Old Branches
echo.
echo ^```bash
echo # Delete local branch
echo git branch -d feature/^<old-feature^>
echo.
echo # Delete remote branch
echo git push origin --delete feature/^<old-feature^>
echo ^```
echo.
echo ## 8️⃣ Staging ^& Committing Tips
echo.
echo ^```bash
echo # Stage specific files
echo git add backend/src/agents/strategy_agent.py
echo.
echo # Commit with detailed message
echo git commit -m "Feature: Add random strategy signals in StrategyAgent"
echo.
echo # Amend last commit ^(if needed^)
echo git commit --amend -m "Updated commit message"
echo.
echo # Push changes
echo git push origin ^<branch-name^>
echo ^```
echo.
echo ## 9️⃣ Quick Status ^& Log
echo.
echo ^```bash
echo git status           # Check current branch ^& staged files
echo git log --oneline    # Short commit history
echo git branch -a        # List all branches
echo git diff             # Show unstaged changes
echo ^```
echo.
echo ---
echo.
echo ✅ This cheat sheet gives you a full Git workflow for QuantumTrade:
echo.
echo - Feature development
echo - Bug fixes / hotfixes
echo - Merges ^& PRs
echo - Version tagging
echo - Cleanup ^& maintenance
) > docs\git_cheat_sheet.md

REM -------------------------------
REM 10️⃣ Git Initialization
REM -------------------------------
echo 🔧 Initializing Git repository...
git init
git checkout -b main
git checkout -b develop
git add .
git commit -m "Initial QuantumTrade project setup with backend, frontend, Docker, scripts, placeholders"

REM -------------------------------
REM 11️⃣ Install dependencies
REM -------------------------------
echo 📦 Installing backend & frontend dependencies...
cd backend
python3 -m venv venv || echo "Venv exists"
REM Note: On Windows, you would typically run: venv\Scripts\activate
REM For this script, we're just creating the venv structure
cd ..\frontend
npm install
cd ..

REM -------------------------------
REM 12️⃣ Generate comprehensive README
REM -------------------------------
echo 📝 Generating comprehensive README.md...
(
echo # QuantumTrade
echo.
echo QuantumTrade is a modular AI-powered trading platform built with Python (FastAPI) and React.  
echo It includes multiple agents, portfolio tracking, risk assessment, and simulated trade execution.
echo.
echo ---
echo.
echo ## **1️⃣ Project Structure**
echo.
echo ^``` 
echo quantumtrade/
echo ├── README.md
echo ├── docs/                    # Guides, API, architecture, deployment
echo ├── scripts/                 # Setup, start, cleanup scripts
echo ├── frontend/                # React frontend
echo │   ├── src/                 # React source code (App.jsx, features)
echo │   ├── public/              # Static assets
echo │   └── package.json
echo ├── backend/                 # Python backend
echo │   ├── src/                 # Core, agents, API, database, config, utils
echo │   └── requirements.txt
echo ├── docker/                  # Dockerfiles and docker-compose
echo ├── logs/                    # Application logs
echo ├── .env.example             # Environment variables template
echo ├── .gitignore
echo └── LICENSE
echo ^```
echo.
echo ---
echo.
echo ## **2️⃣ Features**
echo.
echo - **AI Agents:** DataAgent, StrategyAgent, RiskAgent, PortfolioAgent, ExecutionAgent  
echo - **Trading Signals:** Random BUY/SELL/HOLD for demo  
echo - **Portfolio Tracking:** Add/list positions  
echo - **Risk Assessment:** Simple %% of account balance  
echo - **Trade Execution:** Simulated execution  
echo - **Frontend:** React pages for Signals, Portfolio, Risk  
echo - **Backend API:** FastAPI endpoints for all agents  
echo.
echo ---
echo.
echo ## **3️⃣ Setup Instructions**
echo.
echo ### **Local Setup**
echo.
echo ^```bash
echo # 1. Clone repo
echo git clone ^<repo-url^> quantumtrade
echo cd quantumtrade
echo.
echo # 2. Run setup script (creates folders, installs dependencies)
echo chmod +x setup_quantumtrade.sh
echo ./setup_quantumtrade.sh
echo.
echo # 3. Start app (backend + frontend)
echo ./scripts/start.sh
echo ^```
echo.
echo Open frontend at http://localhost:5173.
echo.
echo ### **Docker Setup**
echo.
echo ^```bash
echo # Build Docker images
echo docker-compose -f docker/docker-compose.yml build
echo.
echo # Start containers
echo docker-compose -f docker/docker-compose.yml up
echo ^```
echo.
echo Backend: http://localhost:8000
echo.
echo Frontend: http://localhost:5173
echo.
echo ---
echo.
echo ## **4️⃣ Testing Features**
echo.
echo ### **Trading Signal:**
echo - Frontend → "Get Signal" button
echo - API: ^`GET /strategy/signal?symbol=BTC-USD^`
echo.
echo ### **Portfolio:**
echo - Frontend → "Load Positions" button
echo - API:
echo   ^```bash
echo   POST /portfolio/add?symbol=BTC-USD^&size=1^&price=30000
echo   GET /portfolio/list
echo   ^```
echo.
echo ### **Risk Assessment:**
echo - Frontend → "Check Risk" button
echo - API: ^`GET /risk/assess?position_size=1000^&account_balance=10000^`
echo.
echo ### **Execute Trade:**
echo - API: ^`POST /execute/trade?symbol=BTC-USD^&action=BUY^&size=1^`
echo.
echo ---
echo.
echo ## **5️⃣ Git Workflow**
echo.
echo See [Git Workflow](docs/git_workflow.md) for detailed instructions.
echo.
echo ---
echo.
echo ## **6️⃣ Cleanup ^& Maintenance**
echo.
echo ### **Remove old Docker artifacts:**
echo ^```bash
echo ./scripts/cleanup.sh
echo ^```
echo.
echo ### **Remove unused volumes/images to save disk space:**
echo ^```bash
echo docker system prune -a
echo ^```
echo.
echo ### **Rotate logs periodically in logs/ folder.**
echo.
echo ---
echo.
echo ## **7️⃣ Optional Enhancements**
echo.
echo - Add historical market data for better signals
echo - Integrate real exchange API for live trading
echo - Add unit/integration tests for all agents and API
echo - Setup CI/CD for automated builds ^& tests
echo - Add monitoring with Prometheus/Grafana
echo.
echo ---
echo.
echo ## **8️⃣ License**
echo.
echo This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
echo.
echo ---
echo.
echo ✅ This README now documents:  
echo.
echo - Full **project structure**  
echo - **Setup instructions** for local ^& Docker  
echo - How to **test all frontend/backend features**  
echo - **Git workflow**  
echo - **Cleanup and maintenance**  
echo.
echo ---
echo.
echo If you want, I can also **update the README automatically in ^`setup_quantumtrade.sh^`**, so after running the script the README is fully populated and ready for the repo.  
echo.
echo Do you want me to do that next?
) > README.md

REM -------------------------------
REM 11️⃣ Finish
REM -------------------------------
echo ✅ QuantumTrade fully setup!
echo Run '.\scripts\start.sh' to start the app.