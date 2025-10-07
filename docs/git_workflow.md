# QuantumTrade Git Workflow

This document describes the Git branching strategy and workflow for the QuantumTrade project.

## 1️⃣ Branch Structure

- **main** → Production-ready, stable code
- **develop** → Integration branch, contains latest tested features
- **feature/<name>** → New feature development
- **bugfix/<name>** → Quick bug fixes
- **release/<version>** → Optional pre-release branch

## 2️⃣ Standard Workflow

### Start a new feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-new-agent
```

### Work on the feature

Add/modify code, agents, API routes, frontend components

Stage and commit changes frequently

```bash
git add .
git commit -m "Add ^<short description^>: ^<details if needed^>"
```

Example:

```bash
git commit -m "Add RiskAgent and risk assessment API route"
```

### Push feature branch to remote

```bash
git push origin feature/add-new-agent
```

### Create a Pull Request (PR)

- Target branch: develop
- Include description and changes

### Code Review & Merge

After approval, merge PR into develop

Pull latest changes:

```bash
git checkout develop
git pull origin develop
```

### Release / Production

```bash
git checkout main
git merge develop
git push origin main
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## 3️⃣ Hotfixes

### Start from main:

```bash
git checkout main
git pull origin main
git checkout -b bugfix/fix-api-error
```

### Fix the bug, commit, push:

```bash
git add .
git commit -m "Fix: corrected API endpoint error"
git push origin bugfix/fix-api-error
```

### Merge into main and develop:

```bash
git checkout main
git merge bugfix/fix-api-error
git push origin main

git checkout develop
git merge bugfix/fix-api-error
git push origin develop
```

## 4️⃣ Tips for a clean repo

- Commit small, logical units
- Keep main always deployable
- Use develop for integration/testing
- Tag every release version
- Regularly clean up old branches:

```bash
git branch -d feature/old-feature
git push origin --delete feature/old-feature
```
