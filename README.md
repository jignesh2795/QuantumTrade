# QuantumTrade

QuantumTrade is a modular AI-powered trading platform built with Python (FastAPI) and React.  
It includes multiple agents, portfolio tracking, risk assessment, and simulated trade execution.

---

## **1️⃣ Project Structure**

```
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
```

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

```bash
# 1. Clone repo
git clone <repo-url> quantumtrade
cd quantumtrade

# 2. Run setup script (creates folders, installs dependencies)
chmod +x setup_quantumtrade.sh
./setup_quantumtrade.sh

# 3. Start app (backend + frontend)
./scripts/start.sh
```

Open frontend at http://localhost:5173.

### **Docker Setup**

```bash
# Build Docker images
docker-compose -f docker/docker-compose.yml build

# Start containers
docker-compose -f docker/docker-compose.yml up
```

Backend: http://localhost:8000

Frontend: http://localhost:5173

---

## **4️⃣ Testing Features**

### **Trading Signal:**
- Frontend → "Get Signal" button
- API: `GET /strategy/signal?symbol=BTC-USD`

### **Portfolio:**
- Frontend → "Load Positions" button
- API:
  ```bash
  POST /portfolio/add?symbol=BTC-USD&size=1&price=30000
  GET /portfolio/list
  ```

### **Risk Assessment:**
- Frontend → "Check Risk" button
- API: `GET /risk/assess?position_size=1000&account_balance=10000`

### **Execute Trade:**
- API: `POST /execute/trade?symbol=BTC-USD&action=BUY&size=1`

---

## **5️⃣ Git Workflow**

### **Branches:**
- `main` → production-ready
- `develop` → ongoing development
- `feature/<name>` → new features
- `bugfix/<name>` → hotfixes

### **Initial Commit:**
Already done in setup script

### **Tag Releases:**
```bash
git tag -a v0.1.0 -m "First working demo"
git push origin v0.1.0
```

---

## **6️⃣ Cleanup & Maintenance**

### **Remove old Docker artifacts:**
```bash
./scripts/cleanup.sh
```

### **Remove unused volumes/images to save disk space:**
```bash
docker system prune -a
```

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

If you want, I can also **update the README automatically in `setup_quantumtrade.sh`**, so after running the script the README is fully populated and ready for the repo.  

Do you want me to do that next?