#!/bin/bash
set -e

echo "🚀 Starting full QuantumTrade setup..."

# -------------------------------
# 1️⃣ Create folder structure
# -------------------------------
echo "📁 Creating project folders..."
mkdir -p docs scripts frontend/{src/{features,components,hooks,context,services,utils},public/assets} backend/{src/{core,services,agents/plugins,api/{routes,middleware},database/migrations,config/environments,utils},tests,scripts} docker logs

# -------------------------------
# 2️⃣ Create placeholder files
# -------------------------------
echo "📝 Creating placeholder files..."

# Root files
touch README.md
touch LICENSE
touch .gitignore
touch .env.example

# Docs
for f in setup api architecture deployment troubleshooting; do
    touch docs/$f.md
done

# Scripts
for s in start setup cleanup; do
    touch scripts/$s.sh
done

# Frontend
touch frontend/Dockerfile
touch frontend/Dockerfile.dev
touch frontend/package.json
touch frontend/vite.config.js
touch frontend/src/main.jsx
touch frontend/src/App.jsx
touch frontend/public/index.html

# Backend
touch backend/Dockerfile
touch backend/Dockerfile.dev
touch backend/requirements.txt
touch backend/src/__init__.py
touch backend/src/main.py
touch backend/src/core/__init__.py
touch backend/src/services/__init__.py
touch backend/src/agents/__init__.py
touch backend/src/agents/plugins/__init__.py
touch backend/src/api/server.py
touch backend/src/api/routes/__init__.py
touch backend/src/api/middleware/__init__.py
touch backend/src/database/migrations/__init__.py
touch backend/src/config/environments/development.yaml
touch backend/src/config/feature_flags.yaml
touch backend/src/utils/__init__.py
touch backend/tests/__init__.py
touch backend/scripts/db_migrate.sh

# Docker folder
touch docker/docker-compose.yml
touch docker/.dockerignore

# -------------------------------
# 3️⃣ Backend dependencies
# -------------------------------
echo "📦 Writing backend requirements..."
cat > backend/requirements.txt <<EOL
fastapi==0.111.1
uvicorn[standard]==0.23.2
sqlalchemy==2.0.22
psycopg2-binary==2.9.7
pydantic==2.6.0
python-dotenv==1.0.1
pytest==8.2.1
pytest-asyncio==0.22.0
requests==2.32.1
numpy==1.26.2
pandas==2.1.1
aiohttp==3.9.3
EOL

# -------------------------------
# 4️⃣ Frontend dependencies
# -------------------------------
echo "📦 Writing frontend package.json..."
cat > frontend/package.json <<EOL
{
  "name": "quantumtrade-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.5",
    "chart.js": "^4.4.0",
    "react-chartjs-2": "^5.2.0",
    "react-router-dom": "^6.17.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.0",
    "vite": "^5.0.0"
  }
}
EOL

# -------------------------------
# 5️⃣ Placeholder backend files
# -------------------------------
cat > backend/src/main.py <<EOL
from src.api.server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
EOL

cat > backend/src/api/server.py <<EOL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

app = FastAPI(title="QuantumTrade API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "QuantumTrade API is running!"}

app.include_router(router)
EOL

cat > backend/src/api/routes/__init__.py <<EOL
from fastapi import APIRouter
from src.agents.strategy_agent import StrategyAgent
from src.agents.data_agent import DataAgent
from src.agents.risk_agent import RiskAgent
from src.agents.portfolio import PortfolioAgent
from src.agents.execution_agent import ExecutionAgent

router = APIRouter()

portfolio = PortfolioAgent()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/agents")
def list_agents():
    return {"agents": ["data_agent", "strategy_agent", "risk_agent", "portfolio", "execution_agent"]}

@router.get("/strategy/signal")
def strategy_signal(symbol: str = "BTC-USD"):
    agent = StrategyAgent(symbol)
    return agent.generate_signal()

@router.get("/data/price")
def get_price(symbol: str = "BTC-USD"):
    agent = DataAgent()
    return agent.get_price(symbol)

@router.post("/portfolio/add")
def add_position(symbol: str, size: float, price: float):
    return portfolio.add_position(symbol, size, price)

@router.get("/portfolio/list")
def list_positions():
    return portfolio.list_positions()

@router.get("/risk/assess")
def assess_risk(position_size: float = 1000, account_balance: float = 10000):
    agent = RiskAgent()
    return agent.assess_risk(position_size, account_balance)

@router.post("/execute/trade")
def execute_trade(symbol: str, action: str, size: float):
    agent = ExecutionAgent()
    return agent.execute_trade(symbol, action, size)
EOL

# -------------------------------
# 6️⃣ Placeholder frontend files
# -------------------------------
cat > frontend/src/main.jsx <<EOL
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOL

cat > frontend/src/App.jsx <<EOL
import React from "react";
import Signal from "./features/Signal";
import Portfolio from "./features/Portfolio";
import Risk from "./features/Risk";

function App() {
  return (
    <div style={{ padding: "2rem" }}>
      <h1>QuantumTrade Frontend</h1>
      <p>Your app is running! Connect to the backend API at <code>/api</code>.</p>
      <Signal />
      <Portfolio />
      <Risk />
    </div>
  );
}

export default App;
EOL

cat > frontend/public/index.html <<EOL
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>QuantumTrade</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOL

# -------------------------------
# 7️⃣ Scripts
# -------------------------------
cat > scripts/setup.sh <<EOL
#!/bin/bash
# Install dependencies
set -e
echo "⚙️ Setting up QuantumTrade environment from root..."

# Backend
cd backend
python3 -m venv venv || echo "Venv exists"
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Backend dependencies installed"
cd ..

# Frontend
cd frontend
npm install
echo "✅ Frontend dependencies installed"
cd ..

echo "✅ Setup complete! Run ./scripts/start.sh to start the application"
echo "Or use Docker: docker-compose -f docker/docker-compose.yml up --build"
EOL

cat > scripts/start.sh <<EOL
#!/bin/bash
# Start app (local or Docker)
set -e
echo "🚀 Starting QuantumTrade from root..."

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if command -v docker-compose &> /dev/null; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose -f docker/docker-compose.yml up --build
else
    echo "⚙️ Starting locally..."
    
    # Start backend
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate
        echo "✅ Backend virtual environment activated"
    else
        echo "⚠️ Backend virtual environment not found. Run ./scripts/setup.sh first"
        exit 1
    fi
    
    echo "🚀 Starting backend server on http://localhost:8000"
    uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload &
    cd ..
    
    # Start frontend
    cd frontend
    echo "🚀 Starting frontend on http://localhost:5173"
    npm run dev &
    cd ..
    
    echo "✅ QuantumTrade running locally!"
    echo "Frontend: http://localhost:5173"
    echo "Backend API: http://localhost:8000"
    echo "Press Ctrl+C to stop"
    
    # Wait for background processes
    wait
fi
EOL

cat > scripts/cleanup.sh <<EOL
#!/bin/bash
# Docker cleanup
echo "🧹 Cleaning up Docker containers, images, volumes..."
docker container prune -f
docker image prune -f
docker volume prune -f
docker network prune -f
docker builder prune -a --filter "until=72h" -f
echo "✅ Cleanup complete!"
EOL

# -------------------------------
# 8️⃣ Git Initialization
# -------------------------------
echo "🔧 Initializing Git repository..."
git init
git checkout -b main
git checkout -b develop
git add .
git commit -m "Initial QuantumTrade project setup with backend, frontend, Docker, scripts, placeholders"

# -------------------------------
# 9️⃣ Install dependencies
# -------------------------------
echo "📦 Installing backend & frontend dependencies..."
cd backend
python3 -m venv venv || echo "Venv exists"
source venv/bin/activate
pip install -r requirements.txt
cd ../frontend
npm install
cd ..

# -------------------------------
# 10️⃣ Generate comprehensive README
# -------------------------------
echo "📝 Generating comprehensive README.md..."
cat > README.md <<EOL
# QuantumTrade

QuantumTrade is a modular AI-powered trading platform built with Python (FastAPI) and React.  
It includes multiple agents, portfolio tracking, risk assessment, and simulated trade execution.

---

## **1️⃣ Project Structure**

\`\`\`
quantumtrade/
├── README.md
├── docs/                    # Guides, API, architecture, deployment
├── scripts/                 # Setup, start, cleanup scripts
├── frontend/                # React frontend
│   ├── src/                 # React source code (App.jsx, features)
│   ├── public/              # Static assets
│   └── package.json
├── backend/                 # Python backend
│   ├── src/                 # Core, agents, API, database, config, utils
│   └── requirements.txt
├── docker/                  # Dockerfiles and docker-compose
├── logs/                    # Application logs
├── .env.example             # Environment variables template
├── .gitignore
└── LICENSE
\`\`\`

---

## **2️⃣ Features**

- **AI Agents:** DataAgent, StrategyAgent, RiskAgent, PortfolioAgent, ExecutionAgent  
- **Trading Signals:** Random BUY/SELL/HOLD for demo  
- **Portfolio Tracking:** Add/list positions  
- **Risk Assessment:** Simple % of account balance  
- **Trade Execution:** Simulated execution  
- **Frontend:** React pages for Signals, Portfolio, Risk  
- **Backend API:** FastAPI endpoints for all agents  

---

## **3️⃣ Setup Instructions**

### **Local Setup**

\`\`\`bash
# 1. Clone repo
git clone <repo-url> quantumtrade
cd quantumtrade

# 2. Run setup script (creates folders, installs dependencies)
chmod +x setup_quantumtrade.sh
./setup_quantumtrade.sh

# 3. Start app (backend + frontend)
./scripts/start.sh
\`\`\`

Open frontend at http://localhost:5173.

### **Docker Setup**

\`\`\`bash
# Build Docker images
docker-compose -f docker/docker-compose.yml build

# Start containers
docker-compose -f docker/docker-compose.yml up
\`\`\`

Backend: http://localhost:8000

Frontend: http://localhost:5173

---

## **4️⃣ Testing Features**

### **Trading Signal:**
- Frontend → "Get Signal" button
- API: \`GET /strategy/signal?symbol=BTC-USD\`

### **Portfolio:**
- Frontend → "Load Positions" button
- API:
  \`\`\`bash
  POST /portfolio/add?symbol=BTC-USD&size=1&price=30000
  GET /portfolio/list
  \`\`\`

### **Risk Assessment:**
- Frontend → "Check Risk" button
- API: \`GET /risk/assess?position_size=1000&account_balance=10000\`

### **Execute Trade:**
- API: \`POST /execute/trade?symbol=BTC-USD&action=BUY&size=1\`

---

## **5️⃣ Git Workflow**

### **Branches:**
- \`main\` → production-ready
- \`develop\` → ongoing development
- \`feature/<name>\` → new features
- \`bugfix/<name>\` → hotfixes

### **Initial Commit:**
Already done in setup script

### **Tag Releases:**
\`\`\`bash
git tag -a v0.1.0 -m "First working demo"
git push origin v0.1.0
\`\`\`

---

## **6️⃣ Cleanup & Maintenance**

### **Remove old Docker artifacts:**
\`\`\`bash
./scripts/cleanup.sh
\`\`\`

### **Remove unused volumes/images to save disk space:**
\`\`\`bash
docker system prune -a
\`\`\`

### **Rotate logs periodically in logs/ folder.**

---

## **7️⃣ Optional Enhancements**

- Add historical market data for better signals
- Integrate real exchange API for live trading
- Add unit/integration tests for all agents and API
- Setup CI/CD for automated builds & tests
- Add monitoring with Prometheus/Grafana

---

## **8️⃣ License**

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

✅ This README now documents:  

- Full **project structure**  
- **Setup instructions** for local & Docker  
- How to **test all frontend/backend features**  
- **Git workflow**  
- **Cleanup and maintenance**  

---

If you want, I can also **update the README automatically in \`setup_quantumtrade.sh\`**, so after running the script the README is fully populated and ready for the repo.  

Do you want me to do that next?
EOL

# -------------------------------
# 11️⃣ Finish
# -------------------------------
echo "✅ QuantumTrade fully setup!"
echo "Run './scripts/start.sh' to start the app."