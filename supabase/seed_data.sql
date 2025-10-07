-- Seed data for QuantumTrade Supabase database

-- Insert sample users
INSERT INTO users (email, password_hash) VALUES 
  ('admin@quantumtrade.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S'),
  ('user1@quantumtrade.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S'),
  ('user2@quantumtrade.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S')
ON CONFLICT (email) DO NOTHING;

-- Insert sample trades
INSERT INTO trades (user_id, asset, trade_type, amount, price) VALUES 
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'BTC-USD', 'BUY', 0.5, 45000.00),
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'ETH-USD', 'BUY', 5.0, 3000.00),
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'BTC-USD', 'SELL', 0.2, 46000.00),
  ((SELECT id FROM users WHERE email = 'user1@quantumtrade.com'), 'AAPL', 'BUY', 10, 150.00),
  ((SELECT id FROM users WHERE email = 'user1@quantumtrade.com'), 'GOOGL', 'BUY', 5, 2500.00)
ON CONFLICT DO NOTHING;

-- Insert sample portfolio data
INSERT INTO portfolio (user_id, asset, quantity, avg_price) VALUES 
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'BTC-USD', 0.3, 45000.00),
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'ETH-USD', 5.0, 3000.00),
  ((SELECT id FROM users WHERE email = 'user1@quantumtrade.com'), 'AAPL', 10, 150.00),
  ((SELECT id FROM users WHERE email = 'user1@quantumtrade.com'), 'GOOGL', 5, 2500.00)
ON CONFLICT DO NOTHING;

-- Insert sample strategy configurations
INSERT INTO strategy_configurations (user_id, strategy_name, asset, is_active, config) VALUES 
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'MovingAverage', 'BTC-USD', true, '{"period": 20, "threshold": 0.02}'),
  ((SELECT id FROM users WHERE email = 'admin@quantumtrade.com'), 'RSI', 'ETH-USD', true, '{"period": 14, "overbought": 70, "oversold": 30}'),
  ((SELECT id FROM users WHERE email = 'user1@quantumtrade.com'), 'BollingerBands', 'AAPL', true, '{"period": 20, "std_dev": 2}')
ON CONFLICT DO NOTHING;