# QuantumTrade Git Cheat Sheet

Quick reference for common Git operations in the QuantumTrade project.

## 1️⃣ Initial Setup

```bash
# Initialize repo (already done if setup script ran)
git init

# Add remote origin
git remote add origin <repo-url>

# Pull latest develop/main
git checkout develop
git pull origin develop
```

## 2️⃣ Creating a New Feature

```bash
# Start feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/<feature-name>

# Work on feature
# ...

# Stage & commit
git add .
git commit -m "Feature: ^<short description^>"

# Push feature branch
git push origin feature/<feature-name>
```

## 3️⃣ Creating a Hotfix / Bugfix

```bash
# Start hotfix from main
git checkout main
git pull origin main
git checkout -b bugfix/<bug-name>

# Fix the bug
# ...

# Stage & commit
git add .
git commit -m "Fix: ^<short description^>"

# Push bugfix branch
git push origin bugfix/<bug-name>
```

## 4️⃣ Pull Request / Merge

```bash
# Merge feature/bugfix into develop
git checkout develop
git pull origin develop
git merge feature/<feature-name>   # or bugfix/<bug-name>
git push origin develop

# Merge develop into main for release
git checkout main
git merge develop
git push origin main
```

## 5️⃣ Tagging a Release

```bash
git checkout main
git pull origin main

# Tag release
git tag -a v<version> -m "Release v^<version^>"
git push origin v<version>
```

Example:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

## 6️⃣ Updating Branches

```bash
# Update your branch with latest develop
git checkout feature/<feature-name>
git pull origin develop
git merge develop
```

## 7️⃣ Cleaning Up Old Branches

```bash
# Delete local branch
git branch -d feature/<old-feature>

# Delete remote branch
git push origin --delete feature/<old-feature>
```

## 8️⃣ Staging & Committing Tips

```bash
# Stage specific files
git add backend/src/agents/strategy_agent.py

# Commit with detailed message
git commit -m "Feature: Add random strategy signals in StrategyAgent"

# Amend last commit (if needed)
git commit --amend -m "Updated commit message"

# Push changes
git push origin <branch-name>
```

## 9️⃣ Quick Status & Log

```bash
git status           # Check current branch & staged files
git log --oneline    # Short commit history
git branch -a        # List all branches
git diff             # Show unstaged changes
```

---

✅ This cheat sheet gives you a full Git workflow for QuantumTrade:

- Feature development
- Bug fixes / hotfixes
- Merges & PRs
- Version tagging
- Cleanup & maintenance
