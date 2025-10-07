# QuantumTrade Git Auto Commit Scripts

This document explains how to use the automated Git commit scripts for the QuantumTrade project.

## Overview

The Git auto-commit scripts automatically detect changes by stage, create clean commit messages, and push them to the correct branch. This ensures a clean Git history and prevents redundant commits.

## Available Scripts

### Unix/Linux/macOS Version

-   **File**: `scripts/git_auto_commit.sh`
-   **Usage**: `bash scripts/git_auto_commit.sh [branch]`

### Windows Version

-   **File**: `scripts/git_auto_commit.bat`
-   **Usage**: `scripts/git_auto_commit.bat [branch]`

## Commit Plan

The script follows this specific commit plan:

| Commit # | Description                               | Folders Watched                                                                          | Commit Message                                                                    |
| -------- | ----------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1        | Initial Project Setup (already completed) | `src/`, `docs/`, `infrastructure/`                                                       | "Initial commit: setup base project structure"                                    |
| 2        | Stage 2: Backend + Frontend Docker Setup  | `backend/`, `frontend/`, `docker-compose.yml`, `.env.example`, `scripts/`                | "Stage 2: Added unified backend + frontend Docker setup with volume optimization" |
| 3        | Stage 3: Supabase Cloud Integration       | `backend/src/database/`, `.env`, `docker-compose.yml`                                    | "Stage 3: Integrated Supabase Cloud database connection"                          |
| 4        | Stage 3.5: Supabase Auth + GitHub CI/CD   | `frontend/src/supabaseClient.js`, `backend/src/api/routes/auth.py`, `.github/workflows/` | "Stage 3.5: Added Supabase Auth (JWT) and GitHub CI/CD pipeline"                  |
| -        | Cleanup                                   | `scripts/cleanup_docker.sh`, `scripts/cleanup_docker.bat`                                | "Added Docker cleanup automation script"                                          |

## Usage

### Default Usage (develop branch)

```bash
# Unix/Linux/macOS
bash scripts/git_auto_commit.sh

# Windows
scripts/git_auto_commit.bat
```

### Specify Branch

```bash
# Unix/Linux/macOS
bash scripts/git_auto_commit.sh main

# Windows
scripts/git_auto_commit.bat main
```

## Features

1. **Automatic Change Detection**: Only commits folders with actual changes
2. **Stage-based Commits**: Groups changes by development stage
3. **Automatic Push**: Pushes commits to the specified branch
4. **Error Prevention**: Checks for Git repository and handles errors gracefully
5. **Cross-platform**: Works on both Unix-like systems and Windows

## Best Practices

1. **Run After Each Stage**: Execute the script after completing each development stage
2. **Check Changes**: Review the changes before running the script
3. **Branch Management**: Work on `develop` branch and merge to `main` when stable
4. **Regular Commits**: Run the script regularly to maintain clean history

## Example Workflow

```bash
# After completing Stage 2
bash scripts/git_auto_commit.sh

# After completing Stage 3
bash scripts/git_auto_commit.sh

# After completing Stage 3.5
bash scripts/git_auto_commit.sh

# Push to main when ready
git checkout main
git merge develop
git push origin main
```

## Troubleshooting

### "No Git repository found"

Initialize Git first:

```bash
git init
git remote add origin <your-repository-url>
```

### Permission Denied

Make the script executable (Unix/Linux/macOS):

```bash
chmod +x scripts/git_auto_commit.sh
```

### No Changes Detected

Ensure you've added files to the staging area or made actual changes to the watched folders.

## Customization

To modify the script behavior:

1. Edit the paths in the `has_changes()` function
2. Adjust commit messages as needed
3. Add or remove stages based on your workflow

The script helps maintain a clean, organized Git history while automating the commit process for the QuantumTrade project.
