-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  password_hash text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create trades table
CREATE TABLE IF NOT EXISTS trades (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  asset text NOT NULL,
  trade_type text CHECK (trade_type IN ('BUY','SELL')),
  amount numeric NOT NULL,
  price numeric NOT NULL,
  timestamp timestamptz DEFAULT now()
);

-- Create portfolio table
CREATE TABLE IF NOT EXISTS portfolio (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  asset text NOT NULL,
  quantity numeric DEFAULT 0,
  avg_price numeric DEFAULT 0
);

-- Create strategy_executions table
CREATE TABLE IF NOT EXISTS strategy_executions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  strategy_name text NOT NULL,
  asset text NOT NULL,
  signal text CHECK (signal IN ('BUY', 'SELL', 'HOLD')),
  confidence numeric,
  executed_at timestamptz DEFAULT now()
);

-- Create strategy_configurations table
CREATE TABLE IF NOT EXISTS strategy_configurations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES users(id),
  strategy_name text NOT NULL,
  asset text NOT NULL,
  is_active boolean DEFAULT true,
  config jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);