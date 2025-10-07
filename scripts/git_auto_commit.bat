@echo off
REM =======================================================
REM 🧠 QuantumTrade Git Auto Commit Script
REM Automates multi-stage commits (Stage 1 → Stage 3.5)
REM =======================================================

setlocal enabledelayedexpansion

set BRANCH=%1
if "%BRANCH%"=="" set BRANCH=develop

echo 🚀 Starting Git Auto Commit for branch: %BRANCH%
git status

REM Ensure Git is initialized
if not exist .git (
  echo ❌ No Git repository found. Initialize first with: git init
  exit /b 1
)

REM Stage 1: Initial setup (already completed)
echo Checking for Stage 1 changes...
git diff --quiet HEAD -- src/ docs/ infrastructure/ 2>nul
if errorlevel 1 (
  echo 📦 Committing Stage 1 changes...
  git add src/ docs/ infrastructure/
  git commit -m "Initial commit: setup base project structure"
  git push origin %BRANCH%
) else (
  echo ✅ No changes detected for Stage 1 (already committed)
)

REM Stage 2: Backend + Frontend Docker Setup
echo Checking for Stage 2 changes...
git diff --quiet HEAD -- backend/ frontend/ docker-compose.yml .env.example scripts/ 2>nul
if errorlevel 1 (
  echo 🐳 Committing Stage 2: Backend + Frontend Docker setup...
  git add backend/ frontend/ docker-compose.yml .env.example scripts/
  git commit -m "Stage 2: Added unified backend + frontend Docker setup with volume optimization"
  git push origin %BRANCH%
) else (
  echo ✅ No changes detected for Stage 2
)

REM Stage 3: Supabase Cloud Integration
echo Checking for Stage 3 changes...
git diff --quiet HEAD -- backend/src/database/ .env docker-compose.yml 2>nul
if errorlevel 1 (
  echo ☁️ Committing Stage 3: Supabase Cloud integration...
  git add backend/src/database/ .env docker-compose.yml
  git commit -m "Stage 3: Integrated Supabase Cloud database connection"
  git push origin %BRANCH%
) else (
  echo ✅ No changes detected for Stage 3
)

REM Stage 3.5: Supabase Auth + CI/CD
echo Checking for Stage 3.5 changes...
git diff --quiet HEAD -- frontend/src/supabaseClient.js backend/src/api/routes/auth.py .github/workflows/ 2>nul
if errorlevel 1 (
  echo 🔐 Committing Stage 3.5: Supabase Auth + GitHub CI/CD...
  git add frontend/src/supabaseClient.js backend/src/api/routes/auth.py .github/workflows/
  git commit -m "Stage 3.5: Added Supabase Auth (JWT) and GitHub CI/CD pipeline"
  git push origin %BRANCH%
) else (
  echo ✅ No changes detected for Stage 3.5
)

REM Cleanup commits (optional)
echo Checking for cleanup script changes...
git diff --quiet HEAD -- scripts/cleanup_docker.sh scripts/cleanup_docker.bat 2>nul
if errorlevel 1 (
  echo 🧹 Committing Docker cleanup script...
  git add scripts/cleanup_docker.sh scripts/cleanup_docker.bat
  git commit -m "Added Docker cleanup automation script"
  git push origin %BRANCH%
) else (
  echo ✅ No cleanup script changes detected
)

echo 🎯 All staged commits complete and pushed to %BRANCH% successfully!