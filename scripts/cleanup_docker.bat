@echo off
echo 🧹 Cleaning unused Docker images, containers, and volumes...
docker system prune -af --volumes
echo ✅ Cleanup complete!