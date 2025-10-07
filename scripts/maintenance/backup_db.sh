#!/bin/bash

# QuantumTrade Database Backup Script

# Create backup directory if it doesn't exist
mkdir -p backups

# Get current timestamp
timestamp=$(date +"%Y%m%d_%H%M%S")

# Backup database
pg_dump -h localhost -U quantumtrade -d quantumtrade > backups/quantumtrade_backup_$timestamp.sql

echo "Database backup created: backups/quantumtrade_backup_$timestamp.sql"
