#!/bin/bash
# Database initialization script

echo "Initializing database..."

# Wait for PostgreSQL to be ready
for i in {1..30}; do
  if pg_isready -h supabase-db -p 5432 -U postgres; then
    echo "PostgreSQL is ready!"
    break
  fi
  echo "Waiting for PostgreSQL to be ready... ($i/30)"
  sleep 2
done

if ! pg_isready -h supabase-db -p 5432 -U postgres; then
  echo "PostgreSQL is not ready after 60 seconds, exiting..."
  exit 1
fi

# Run database initialization
cd /app
python -c "
import sys
import time
sys.path.append('/app/src')

# Wait a bit more for the database to be fully ready
time.sleep(5)

try:
    from database.connection import init_database
    init_database()
    print('Database initialization completed!')
except Exception as e:
    print(f'Error during database initialization: {e}')
    # Don't exit here as we want the container to continue running
"

echo "Database initialization script completed!"