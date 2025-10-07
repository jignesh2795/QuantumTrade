# Supabase Configuration for QuantumTrade

## Overview

This document explains how to configure QuantumTrade to use the Supabase Cloud project at https://jstuvjquxrciaazrsedx.supabase.co.

## Prerequisites

1. A Supabase account
2. Access to the Supabase project at https://jstuvjquxrciaazrsedx.supabase.co
3. Supabase API keys (Anon Key, Service Role Key, JWT Secret)

## Configuration Steps

### 1. Run the Configuration Script

#### For Unix/Linux/macOS:

```bash
bash scripts/configure_supabase.sh
```

#### For Windows:

```cmd
scripts\configure_supabase.bat
```

### 2. Update Environment Variables

After running the script, update the following values in your `.env` file:

**Note**: The `.env` file is intentionally ignored by Git for security reasons (credentials should never be committed to version control). If you don't have a `.env` file yet, copy the `.env.example` file to create one:

```bash
# Unix/Linux/macOS
cp .env.example .env

# Windows
copy .env.example .env
```

1. **DATABASE_URL**: Replace `<USER>` and `<PASSWORD>` with your Supabase database credentials
2. **SUPABASE_ANON_KEY**: Get from your Supabase project dashboard
3. **SUPABASE_SERVICE_ROLE_KEY**: Get from your Supabase project dashboard
4. **SUPABASE_JWT_SECRET**: Get from your Supabase project dashboard

### 3. Finding Your Supabase Credentials

1. Go to https://app.supabase.com/
2. Select your project (jstuvjquxrciaazrsedx)
3. Navigate to Settings > API
4. Copy the required keys from the **Project API keys** section (not the legacy keys):
    - Project URL (should be https://jstuvjquxrciaazrsedx.supabase.co)
    - **anon key** (for frontend - this is labeled as the 'public' key in the dashboard)
    - **service_role key** (for backend - this is the secret key with full access, same as SUPABASE_SERVICE_ROLE_KEY)
    - JWT Secret (for authentication)

**Note**: In the Supabase dashboard, the 'anon key' is labeled as the 'public' key, and the 'service_role key' is the secret key that should only be used in backend applications.

**Note**: In the Supabase dashboard, the 'anon key' is labeled as the 'public' key. This is the key you should use for frontend applications.

**Note**: Use the new API keys, not the legacy ones. The new keys provide better security and more granular permissions.

### 4. Database Connection

The database connection string format for Supabase is:

```
postgresql://<USER>:<PASSWORD>@jstuvjquxrciaazrsedx.supabase.co:5432/postgres
```

Replace `<USER>` and `<PASSWORD>` with your actual database credentials.

## Testing the Configuration

### 1. Backend Test

Run the backend database connection test:

```bash
cd backend
python -m src.database.supabase_client
```

### 2. Frontend Test

Start the frontend and check the browser console for Supabase connection messages.

## Troubleshooting

### Common Issues

1. **Connection Refused**: Verify the Supabase project is active and the credentials are correct
2. **Authentication Failed**: Check that the API keys are correct and have the proper permissions
3. **Network Issues**: Ensure there are no firewall rules blocking access to Supabase

### Debugging Steps

1. Check the application logs for database connection errors
2. Verify the environment variables are loaded correctly
3. Test the database connection manually with a PostgreSQL client

## Security Best Practices

1. Never commit sensitive credentials to version control
2. Use environment variables for all sensitive information
3. Rotate API keys regularly
4. Restrict database user permissions to minimum required
5. Use SSL/TLS for all database connections

## Additional Resources

-   [Supabase Documentation](https://supabase.com/docs)
-   [QuantumTrade Database Documentation](docs/database.md)
-   [Environment Configuration Guide](docs/configuration.md)
