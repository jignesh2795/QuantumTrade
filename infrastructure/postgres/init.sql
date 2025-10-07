-- QuantumTrade PostgreSQL Initialization Script

-- Create database
CREATE DATABASE quantumtrade;

-- Connect to database
\c quantumtrade;

-- Create tables
CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    action VARCHAR(10) NOT NULL,
    size DECIMAL NOT NULL,
    price DECIMAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    strategy_id VARCHAR(50),
    commission DECIMAL DEFAULT 0.0,
    slippage DECIMAL DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'filled'
);

CREATE TABLE IF NOT EXISTS positions (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    size DECIMAL NOT NULL,
    avg_price DECIMAL NOT NULL,
    current_price DECIMAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open_price DECIMAL NOT NULL,
    high_price DECIMAL NOT NULL,
    low_price DECIMAL NOT NULL,
    close_price DECIMAL NOT NULL,
    volume DECIMAL NOT NULL,
    interval VARCHAR(10) DEFAULT '1d'
);

CREATE TABLE IF NOT EXISTS strategy_results (
    id SERIAL PRIMARY KEY,
    strategy_name VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    initial_capital DECIMAL NOT NULL,
    final_capital DECIMAL NOT NULL,
    total_return DECIMAL NOT NULL,
    sharpe_ratio DECIMAL,
    max_drawdown DECIMAL,
    win_rate DECIMAL,
    total_trades INTEGER NOT NULL,
    profitable_trades INTEGER,
    config TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    value DECIMAL NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    context VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS backtest_results (
    id SERIAL PRIMARY KEY,
    strategy VARCHAR(100) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    initial_capital DECIMAL NOT NULL,
    final_capital DECIMAL NOT NULL,
    total_return DECIMAL NOT NULL,
    max_drawdown DECIMAL NOT NULL,
    sharpe_ratio DECIMAL NOT NULL,
    win_rate DECIMAL NOT NULL,
    total_trades INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS configurations (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol);
CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp);
CREATE INDEX IF NOT EXISTS idx_positions_symbol ON positions(symbol);
CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol);
CREATE INDEX IF NOT EXISTS idx_market_data_timestamp ON market_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);

-- Insert default configuration
INSERT INTO configurations (key, value, description) VALUES 
    ('max_position_size_percent', '5.0', 'Maximum position size as percentage of portfolio'),
    ('max_portfolio_risk_percent', '2.0', 'Maximum portfolio risk percentage'),
    ('stop_loss_percent', '5.0', 'Default stop loss percentage'),
    ('max_drawdown_limit', '20.0', 'Maximum drawdown limit percentage'),
    ('max_leverage', '2.0', 'Maximum leverage allowed');

-- Create default user (admin/admin123)
INSERT INTO users (username, email, hashed_password, is_admin) VALUES 
    ('admin', 'admin@quantumtrade.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', TRUE);

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE trades TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE positions TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE market_data TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE strategy_results TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE performance_metrics TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE backtest_results TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE users TO quantumtrade;
GRANT ALL PRIVILEGES ON TABLE configurations TO quantumtrade;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO quantumtrade;