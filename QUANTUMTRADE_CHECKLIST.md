# QuantumTrade Full Setup & Checklist (With Git)

## 1️⃣ Git Setup

### Initialize Git in the project root:
```bash
git init
```

### Create .gitignore (already part of skeleton):
```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# Node
node_modules/
dist/
*.log

# Docker
docker-compose.override.yml
*.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Create main branches:
```bash
git checkout -b main      # stable production-ready code
git checkout -b develop   # development branch
```

### Commit initial skeleton:
```bash
git add .
git commit -m "Initial QuantumTrade project skeleton with backend, frontend, Docker, scripts, and placeholders"
```

### Optional: Set up remote origin:
```bash
git remote add origin <repo-url>
git push -u origin main
```

## 2️⃣ Project Setup Checklist

| Step | Description | Done |
|------|-------------|------|
| ✅ | Generate folder structure (backend, frontend, scripts, docker, docs, logs) | |
| ✅ | Populate placeholder backend files (main.py, server.py, routes, core, utils) | |
| ✅ | Populate placeholder frontend files (main.jsx, App.jsx, index.html) | |
| ✅ | Create requirements.txt and package.json with pinned versions | |
| ✅ | Setup scripts/setup.sh for local dependency install | |
| ✅ | Setup scripts/start.sh to run backend + frontend locally or Docker | |
| ✅ | Setup scripts/cleanup.sh for Docker cache cleanup | |
| ✅ | Add Dockerfiles (backend, frontend, dev + prod variants) | |
| ✅ | Add docker-compose.yml with cached volumes for dependencies | |
| ✅ | Configure .env.example for environment variables | |
| ✅ | Setup docs/ with setup, API, architecture, deployment, troubleshooting guides | |
| ✅ | Initialize Git repo and create main/develop branches | |
| ✅ | Setup .gitignore | |
| ✅ | Optional: Add sample AI agent and trading logic placeholders | |
| ✅ | Optional: Add test folders with unit/integration/fixtures placeholders | |
| ✅ | Optional: Add logging/monitoring configuration (logs/, prometheus, etc.) | |

## 3️⃣ Root-Run Command

After cloning, run all setup in one command:

```bash
# Make script executable
chmod +x setup_quantumtrade.sh

# Run full setup (skeleton, dependencies, Docker, Git init)
./setup_quantumtrade.sh

# Start app locally or via Docker
./scripts/start.sh
```

## 4️⃣ Git Best Practices

### Branching:
- `main` → production
- `develop` → daily development
- `feature/<feature-name>` → for new features
- `bugfix/<issue>` → for hotfixes

### Commits: Use meaningful messages, e.g.:
- `feat: add strategy_agent placeholder`
- `fix: correct API route /agents`
- `chore: update Dockerfile with cached volumes`

### Versioning:
Tag releases:
```bash
git tag -a v0.1.0 -m "Initial working version"
git push origin v0.1.0
```

### Remote Repo: 
Push main and develop branches to remote regularly.

### Optional CI/CD: 
Integrate GitHub Actions or GitLab CI for automated tests and Docker builds.

## 5️⃣ Optional Enhancements

- [ ] Add pre-commit hooks to check formatting & linting
- [ ] Add docker volumes for DB so data persists across container rebuilds
- [ ] Add sample seed data for testing AI agents and portfolio
- [ ] Add unit/integration test templates for backend + frontend

## ✅ Next Step Prompt for You

You can now run the full setup including Git from root with:

```bash
# Clone repo
git clone <repo-url> quantumtrade
cd quantumtrade

# Run full setup (creates folders, placeholders, installs dependencies, sets up Docker)
chmod +x setup_quantumtrade.sh
./setup_quantumtrade.sh

# Initialize Git & branches
git init
git checkout -b main
git checkout -b develop
git add .
git commit -m "Initial QuantumTrade project setup with Git, Docker, frontend & backend placeholders"

# Start app
./scripts/start.sh
```

This ensures:
- Root-run ready (local & Docker)
- Full folder + file structure
- Dependencies installed & cached
- Git version control initialized
- Cleanup script for Docker storage