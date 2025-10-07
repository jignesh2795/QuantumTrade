#!/bin/bash

# QuantumTrade Local Supabase Initialization Script
# Sets up and starts local Supabase instance

echo "🚀 Initializing local Supabase instance..."

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null
then
    echo "❌ Supabase CLI is not installed. Please install it first:"
    echo "   npm install -g supabase"
    exit 1
fi

# Start Supabase local development setup
echo "Starting Supabase local development setup..."
supabase start

# Apply migrations
echo "Applying database migrations..."
supabase db reset

# Seed initial data
echo "Seeding initial data..."
supabase db seed

echo "✅ Supabase initialization complete!"
echo "Supabase Studio: http://localhost:54323"
echo "Supabase API: http://localhost:54321"