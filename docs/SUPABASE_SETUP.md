# Supabase Setup Guide

## 📋 Prerequisites

Before setting up Supabase, ensure you have:

-   A Supabase account (free tier available at [supabase.com](https://supabase.com))
-   QuantumTrade project cloned locally
-   Docker and Docker Compose installed (for local development)

## 🚀 Creating a Supabase Project

### 1. Sign Up and Log In

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" or "Sign in"
3. Complete the sign-up process

### 2. Create New Project

1. Click "New Project" in your Supabase dashboard
2. Enter project details:
    - **Name**: QuantumTrade
    - **Database Password**: Set a strong password
    - **Region**: Choose the region closest to your users
3. Click "Create new project"

### 3. Wait for Project Initialization

Supabase will take 1-2 minutes to set up your project. You'll see a loading screen during this time.

## 🔑 Getting Project Credentials

### 1. Access Project Settings

1. Once your project is ready, click on it in the dashboard
2. In the left sidebar, click the "Settings" gear icon
3. Click "API" in the settings menu

### 2. Copy Required Keys

You'll need these values for your `.env` file:

-   **Project URL**: Copy the "URL" value
-   **anon key**: Copy the "anon public" key
-   **service_role key**: Copy the "service_role secret" key

### 3. Update Environment Variables

Create or update your `.env` file in the project root:

```env
SUPABASE_URL=your_project_url_here
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
DATABASE_URL=your_project_url_here (same as SUPABASE_URL)
```

## 🗄️ Database Setup

### 1. Access SQL Editor

1. In your Supabase project dashboard
2. Click "SQL Editor" in the left sidebar
3. You can now run SQL queries

### 2. Run Initial Schema

Execute the initial schema setup:

```sql
-- Create trades table
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    strategy VARCHAR(50),
    user_id UUID REFERENCES auth.users(id)
);

-- Create positions table
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    avg_price DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id)
);

-- Create strategies table
CREATE TABLE strategies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parameters JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id)
);

-- Create performance_metrics table
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    strategy_id INTEGER REFERENCES strategies(id),
    metric_name VARCHAR(50) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_id UUID REFERENCES auth.users(id)
);
```

### 3. Set Up Row Level Security (RLS)

Enable RLS for each table:

```sql
-- Enable RLS
ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE strategies ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view their own trades" ON trades
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own trades" ON trades
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own positions" ON positions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own positions" ON positions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own strategies" ON strategies
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own strategies" ON strategies
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own metrics" ON performance_metrics
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own metrics" ON performance_metrics
    FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## 🔐 Authentication Setup

### 1. Enable Email Authentication

1. In your Supabase project dashboard
2. Click "Authentication" in the left sidebar
3. Click "Settings" tab
4. Under "Email Auth", ensure "Enable email signup" is checked
5. Optionally configure email templates

### 2. Configure Auth Policies

The database policies created above already handle authentication for data access.

### 3. Test Authentication

You can test authentication using the Supabase auth interface or by running the application.

## 🔄 Realtime Setup

### 1. Enable Realtime

1. In your Supabase project dashboard
2. Click "Database" in the left sidebar
3. Click "Replication" tab
4. Enable replication for the tables you want to listen to:
    - trades
    - positions
    - strategies
    - performance_metrics

### 2. Configure Realtime Subscriptions

The application automatically subscribes to changes in these tables.

## 📦 Storage Setup (Optional)

If you plan to store model artifacts or reports:

### 1. Create Storage Bucket

1. In your Supabase project dashboard
2. Click "Storage" in the left sidebar
3. Click "Create Bucket"
4. Name it "quantumtrade" or similar
5. Set visibility as needed

### 2. Configure Storage Policies

```sql
-- Allow users to read and write to their own files
INSERT INTO storage.buckets (id, name)
VALUES ('quantumtrade', 'quantumtrade');

CREATE POLICY "Users can read their own files" ON storage.objects
    FOR SELECT USING (bucket_id = 'quantumtrade' AND auth.uid() = owner);

CREATE POLICY "Users can insert their own files" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'quantumtrade' AND auth.uid() = owner);

CREATE POLICY "Users can update their own files" ON storage.objects
    FOR UPDATE USING (bucket_id = 'quantumtrade' AND auth.uid() = owner);

CREATE POLICY "Users can delete their own files" ON storage.objects
    FOR DELETE USING (bucket_id = 'quantumtrade' AND auth.uid() = owner);
```

## 🧪 Testing the Connection

### 1. Run the Application

```bash
./scripts/start.sh
```

### 2. Check Backend Health

Visit `http://localhost:8000/health` to verify the backend can connect to Supabase.

### 3. Test Authentication

Try to log in through the frontend to verify authentication is working.

### 4. Verify Database Operations

Perform some actions in the application that should create database entries, then check in the Supabase SQL editor.

## 🛠️ Troubleshooting

### Common Issues

#### Connection Refused

-   Verify your `SUPABASE_URL` is correct
-   Check that your Supabase project is active
-   Ensure you have internet connectivity

#### Authentication Failed

-   Verify your `SUPABASE_ANON_KEY` is correct
-   Check that email authentication is enabled
-   Ensure your user account exists

#### Database Operations Failing

-   Verify RLS policies are correctly set up
-   Check that your user has the necessary permissions
-   Ensure tables exist with correct schema

#### Realtime Not Working

-   Verify replication is enabled for your tables
-   Check that you're subscribed to the correct channels
-   Ensure your Supabase client is properly configured

### Debugging Steps

1. **Check Supabase Dashboard Logs**

    - In your Supabase project, go to "Settings" → "Logs"
    - Look for any error messages

2. **Verify Environment Variables**

    ```bash
    cat .env
    ```

    Ensure all Supabase-related variables are set correctly

3. **Test Connection Manually**

    ```bash
    curl -I $SUPABASE_URL
    ```

    Should return HTTP 200

4. **Check Application Logs**
    ```bash
    docker compose logs backend
    ```

## 🔒 Security Best Practices

### API Keys

-   Never commit API keys to version control
-   Use environment variables for all sensitive data
-   Rotate keys periodically

### Database Security

-   Use Row Level Security for all tables
-   Limit permissions to only what's necessary
-   Regularly audit access policies

### Authentication

-   Enforce strong password requirements
-   Implement rate limiting for login attempts
-   Use multi-factor authentication when possible

## 🔄 Sync with Local Development

For local development with Supabase sync:

1. Ensure your local `.env` file has the correct Supabase credentials
2. Run the sync script:
    ```bash
    ./scripts/sync_supabase.sh
    ```
3. Verify data is syncing between local and cloud databases

## 📚 Additional Resources

-   [Supabase Documentation](https://supabase.com/docs)
-   [Supabase Auth Guide](https://supabase.com/docs/guides/auth)
-   [Supabase Database Guide](https://supabase.com/docs/guides/database)
-   [Supabase Realtime Guide](https://supabase.com/docs/guides/realtime)
