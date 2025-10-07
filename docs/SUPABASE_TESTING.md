# Supabase Connection Testing

## Overview

This document explains how to test your Supabase configuration to ensure all keys are correctly set up.

## Testing Script

A testing script is provided at `scripts/test_supabase_connection.py` that verifies:

1. All required environment variables are set
2. Database connection is working
3. Supabase client can connect successfully

## Running the Test

### Prerequisites

Make sure you have:

1. Updated your `.env` file with all Supabase credentials
2. Installed all required dependencies

### Running the Test Script

```bash
# Navigate to the project root
cd /path/to/quantumtrade

# Run the test script
python scripts/test_supabase_connection.py
```

### Expected Output

If all configurations are correct, you should see output similar to:

```
🔍 Testing Supabase Configuration...
==================================================
✅ SUPABASE_URL: https://jstuvjquxrciaazrsedx.supabase.co
✅ SUPABASE_ANON_KEY: ****************************************
✅ SUPABASE_SERVICE_ROLE_KEY: ****************************************
✅ DATABASE_URL: jstuvjquxrciaazrsedx.supabase.co:5432/postgres

🔌 Testing Database Connection...
✅ Database connection successful!

🎉 All Supabase configurations are set correctly!
```

### Troubleshooting

If the test fails, check:

1. **Missing Environment Variables**: Ensure all required variables are set in your `.env` file
2. **Incorrect Credentials**: Verify your Supabase keys are correct
3. **Network Issues**: Ensure you can reach the Supabase servers
4. **Database Permissions**: Check that your database user has the correct permissions

## Manual Verification

You can also manually verify your configuration by checking the `.env` file:

```bash
# View your configuration (be careful not to expose keys publicly)
cat .env | grep SUPABASE
cat .env | grep DATABASE_URL
```

## Security Notes

-   Never commit your `.env` file to version control
-   The testing script masks sensitive keys in the output
-   Regularly rotate your API keys for security
