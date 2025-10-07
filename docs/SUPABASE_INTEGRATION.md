# Supabase Cloud Integration for QuantumTrade

## Overview

This document provides instructions for configuring QuantumTrade to use the Supabase Cloud project at https://jstuvjquxrciaazrsedx.supabase.co.

## Current Configuration

The QuantumTrade project currently uses a local PostgreSQL database for development. To switch to Supabase Cloud, you'll need to update the environment configuration.

## Configuration Steps

### 1. Update Environment Variables

Update your `.env` file with the Supabase Cloud configuration:

```env
# Database Configuration (Supabase Cloud)
DATABASE_URL=postgresql://<USER>:<PASSWORD>@jstuvjquxrciaazrsedx.supabase.co:5432/postgres

# Supabase API
SUPABASE_URL=https://jstuvjquxrciaazrsedx.supabase.co
SUPABASE_ANON_KEY=<your_anon_key>
SUPABASE_SERVICE_ROLE_KEY=<your_service_role_key>

# Optional (Auth)
SUPABASE_JWT_SECRET=<your_supabase_jwt_secret>
```

### 2. Update Frontend Configuration

Update the frontend environment variables in your `.env` file:

```env
# Frontend Configuration
VITE_SUPABASE_URL=https://jstuvjquxrciaazrsedx.supabase.co
VITE_SUPABASE_ANON_KEY=<your_anon_key>
```

### 3. Update Docker Configuration

If using Docker, update the docker-compose.yml to remove the local PostgreSQL service and use the Supabase Cloud connection.

## Required Information

To complete the configuration, you'll need:

1. **Database User Credentials**:

    - Username
    - Password

2. **Supabase API Keys**:
    - Anon Key (for frontend)
    - Service Role Key (for backend)
    - JWT Secret (for authentication)

## Testing the Connection

After updating the configuration:

1. Restart the application
2. Check the logs for successful database connection
3. Verify that the frontend can connect to Supabase

## Troubleshooting

### Connection Issues

If you encounter connection issues:

1. Verify the DATABASE_URL format
2. Check that the Supabase project is active
3. Ensure the credentials are correct
4. Verify network connectivity to Supabase

### Authentication Issues

If authentication fails:

1. Check the SUPABASE_ANON_KEY and SUPABASE_SERVICE_ROLE_KEY
2. Verify the JWT configuration
3. Ensure the Supabase Auth settings are correct

## Security Considerations

1. Never commit sensitive credentials to version control
2. Use environment variables for all sensitive information
3. Rotate API keys regularly
4. Restrict database user permissions to minimum required

## Next Steps

1. Obtain the required credentials from your Supabase dashboard
2. Update the environment configuration
3. Test the connection
4. Deploy the application
