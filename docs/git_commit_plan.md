# QuantumTrade Git Commit Plan

This document outlines the structured Git commit plan for the QuantumTrade project, ensuring a clean and organized version history.

## Commit Plan Overview

| Commit # | Description                              | Status     |
| -------- | ---------------------------------------- | ---------- |
| 1        | Initial Project Setup                    | ✅ Done    |
| 2        | Stage 2: Backend + Frontend Docker Setup | ⏳ Next    |
| 3        | Stage 3: Supabase Cloud Integration      | 🔜 After 2 |
| 4        | Stage 3.5: Supabase Auth + GitHub CI/CD  | 🔜 After 3 |

## Detailed Commit Descriptions

### ✅ Commit #1 — Initial Project Setup

**Status**: Already completed

**Message example**:

```
Initial commit: setup base project structure
```

### 🧱 Commit #2 — Stage 2: Backend + Frontend Docker Setup

**Includes**:

-   Backend service configuration
-   Frontend service configuration
-   Unified docker-compose.yml
-   .env.example file
-   Volume optimization
-   Cleanup scripts

**Run**:

```bash
git add .
git commit -m "Stage 2: Added unified backend + frontend Docker setup with volume optimization"
```

### ☁️ Commit #3 — Stage 3: Supabase Cloud Integration

**Adds**:

-   .env Supabase variables
-   Supabase database connection
-   Backend DB configuration
-   Updated compose removing local Postgres

**Run**:

```bash
git add .
git commit -m "Stage 3: Integrated Supabase Cloud database connection"
```

### 🔐 Commit #4 — Stage 3.5: Supabase Auth + GitHub CI/CD

**Adds**:

-   Supabase email/password auth
-   Frontend login page
-   Backend JWT verification
-   .github/workflows/deploy.yml (CI/CD)
-   Docker cleanup optimization

**Run**:

```bash
git add .
git commit -m "Stage 3.5: Added Supabase Auth (JWT) and GitHub CI/CD pipeline"
```

### 🧹 Optional between commits

If you ever remove caches or large Docker artifacts:

```bash
bash scripts/cleanup_docker.sh
git add scripts/cleanup_docker.sh
git commit -m "Added Docker cleanup automation script"
```

## 🔄 After Each Stage Commit

Push to GitHub:

```bash
git push origin develop
```

## 💡 Git Workflow Tips

**Branch Strategy**:

-   Keep `main` for stable production releases
-   Work on `develop` (as you are doing now)
-   When you finish a stage, you can merge it into `main`:

```bash
git checkout main
git merge develop
git push origin main
```

## Automated Git Commit Scripts

To simplify this process, automated scripts are available:

### Unix/Linux/macOS Version

```bash
bash scripts/git_auto_commit.sh
```

### Windows Version

```bash
scripts/git_auto_commit.bat
```

These scripts will automatically detect changes by stage folders and create appropriate commits with the correct messages.
