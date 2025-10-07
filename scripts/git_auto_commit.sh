#!/bin/bash
# =======================================================
# 🧠 QuantumTrade Git Auto Commit Script
# Automates multi-stage commits (Stage 1 → Stage 3.5)
# =======================================================

# Safety settings
set -e

BRANCH=${1:-develop}

echo "🚀 Starting Git Auto Commit for branch: $BRANCH"
git status

# Ensure Git is initialized
if [ ! -d .git ]; then
  echo "❌ No Git repository found. Initialize first with: git init"
  exit 1
fi

# Function to check if there are changes in specific paths
has_changes() {
  local paths="$1"
  # Check if any of the paths have changes
  if git diff --quiet HEAD -- $paths 2>/dev/null; then
    return 1  # No changes
  else
    return 0  # Has changes
  fi
}

# Stage 1: Initial setup (already completed)
STAGE1_PATHS="src/ docs/ infrastructure/"
if has_changes "$STAGE1_PATHS"; then
  echo "📦 Committing Stage 1 changes..."
  git add $STAGE1_PATHS
  git commit -m "Initial commit: setup base project structure"
  git push origin $BRANCH
else
  echo "✅ No changes detected for Stage 1 (already committed)"
fi

# Stage 2: Backend + Frontend Docker Setup
STAGE2_PATHS="backend/ frontend/ docker-compose.yml .env.example scripts/"
if has_changes "$STAGE2_PATHS"; then
  echo "🐳 Committing Stage 2: Backend + Frontend Docker setup..."
  git add $STAGE2_PATHS
  git commit -m "Stage 2: Added unified backend + frontend Docker setup with volume optimization"
  git push origin $BRANCH
else
  echo "✅ No changes detected for Stage 2"
fi

# Stage 3: Supabase Cloud Integration
STAGE3_PATHS="backend/src/database/ .env docker-compose.yml"
if has_changes "$STAGE3_PATHS"; then
  echo "☁️ Committing Stage 3: Supabase Cloud integration..."
  git add $STAGE3_PATHS
  git commit -m "Stage 3: Integrated Supabase Cloud database connection"
  git push origin $BRANCH
else
  echo "✅ No changes detected for Stage 3"
fi

# Stage 3.5: Supabase Auth + CI/CD
STAGE35_PATHS="frontend/src/supabaseClient.js backend/src/api/routes/auth.py .github/workflows/"
if has_changes "$STAGE35_PATHS"; then
  echo "🔐 Committing Stage 3.5: Supabase Auth + GitHub CI/CD..."
  git add $STAGE35_PATHS
  git commit -m "Stage 3.5: Added Supabase Auth (JWT) and GitHub CI/CD pipeline"
  git push origin $BRANCH
else
  echo "✅ No changes detected for Stage 3.5"
fi

# Cleanup commits (optional)
CLEANUP_PATHS="scripts/cleanup_docker.sh scripts/cleanup_docker.bat"
if has_changes "$CLEANUP_PATHS"; then
  echo "🧹 Committing Docker cleanup script..."
  git add $CLEANUP_PATHS
  git commit -m "Added Docker cleanup automation script"
  git push origin $BRANCH
else
  echo "✅ No cleanup script changes detected"
fi

echo "🎯 All staged commits complete and pushed to $BRANCH successfully!"