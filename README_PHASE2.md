# QuantumTrade - Phase 2: Real Trading Ready

## 🎉 What's New in Phase 2

### Risk Management (Guard Agent)
- ✅ Daily loss limits with circuit breaker
- ✅ Maximum drawdown protection
- ✅ Automatic position sizing
- ✅ Stop-loss and take-profit automation
- ✅ Real-time risk monitoring

### Real Broker Integration
- ✅ Binance API integration
- ✅ Testnet support for safe testing
- ✅ Live trading capability
- ✅ Real-time price feeds
- ✅ Order execution and tracking

### Notifications
- ✅ Email alerts for trades
- ✅ Risk alerts
- ✅ Daily summaries
- ✅ Circuit breaker notifications

### Safety Features
- ✅ Paper trading mode
- ✅ Testnet mode for safe testing
- ✅ Dry run mode (simulate orders)
- ✅ Manual confirmation required for live trading
- ✅ Automatic position closure on risk triggers

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Binance API Keys

**For Testing (Start Here):**
- Go to https://testnet.binance.vision/
- Generate API keys
- Fund with fake USDT

**For Live Trading:**
- Go to https://www.binance.com/
- Create API keys with trading permissions
- Set IP restrictions

### 3. Configure .env
```bash
cp .env.example .env
nano .env
```

Update these settings:
```env
TRADING_MODE=live
USE_TESTNET=true
API_KEY=your_api_key
API_SECRET=your_secret_key

# Start conservative
MAX_POSITION_SIZE=0.05
MAX_DAILY_LOSS=0.01
MAX_DRAWDOWN=0.05
```

### 4. Test Connection
```bash
python scripts/test_binance_connection.py
```

Expected output:
```
✅ ALL TESTS PASSED
You're ready to start trading!
```

### 5. Test Risk Management
```bash
python scripts/check_risk_limits.py
```

### 6. Start Trading
```bash
# Start with testnet
python main.py
```

## 📊 Usage Examples

### Paper Trading (No Real Money)
```bash
# .env settings
TRADING_MODE=paper
```

### Testnet Trading (Fake Money)
```bash
# .env settings
TRADING_MODE=live
USE_TESTNET=true
API_KEY=your_testnet_key
API_SECRET=your_testnet_secret
```

### Live Trading (Real Money)
```bash
# .env settings
TRADING_MODE=live
USE_TESTNET=false
API_KEY=your_real_key
API_SECRET=your_real_secret
INITIAL_CAPITAL=50  # Start small!
```

## 🛡️ Risk Management

### Daily Loss Limit
Automatically stops trading if daily loss exceeds threshold:
```env
MAX_DAILY_LOSS=0.02  # 2% daily loss limit
```

### Maximum Drawdown
Stops trading if drawdown from peak exceeds limit:
```env
MAX_DRAWDOWN=0.10  # 10% max drawdown
```

### Position Sizing
Automatically calculates safe position size:
```env
MAX_POSITION_SIZE=0.1  # Max 10% per trade
```

### Stop-Loss & Take-Profit
Set automatically on every trade:
```env
STOP_LOSS_PCT=0.02    # 2% stop loss
TAKE_PROFIT_PCT=0.04  # 4% take profit
```

## 📧 Email Notifications

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Google Account → Security → App passwords
3. Update .env:
```env
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=your_email@gmail.com
```

### Notifications You'll Get
- ✅ Trade executions
- ⚠️ Risk alerts
- 🚨 Circuit breaker triggers
- 📊 Daily summaries

## 📈 Example Output
```
============================================================
🚀 QUANTUMTRADE TRADING ENGINE - PHASE 2
============================================================
Mode: LIVE
Exchange: binance
⚠️  LIVE TRADING ENABLED - Testnet
Symbol: BTCUSDT
Strategy: SMA_10_30
Capital: $10,000.00
Risk Management: ON 🛡️
============================================================

🔌 Connecting to Binance Testnet...
✅ Connected to Binance successfully
✅ Authentication successful | Account type: SPOT
🛡️  Risk Manager initialized | Max Position: 5.0%, Max Daily Loss: 1.0%
📧 Email notifications enabled

------------------------------------------------------------
📊 Market Update | BTCUSDT @ $43,125.50
💰 Balance: $10,000.00 | Total: $10,000.00 | P&L: $0.00 (0.00%)
🛡️  Risk: Daily P&L: 0.00% | Drawdown: 0.00% | Circuit Breaker: 🟢 OK
🎯 Signal: BUY | Confidence: 0.75% | Bullish crossover

🔵 Executing BUY order | 0.011583 BTCUSDT @ $43,125.50 | SL: $42,263.00 | TP: $44,850.52
✅ BUY order filled | Order ID: 12345678

------------------------------------------------------------
📊 Market Update | BTCUSDT @ $44,892.30
💰 Balance: $0.00 | Total: $10,519.80 | P&L: $519.80 (5.20%)
🛡️  Risk: Daily P&L: 5.20% | Drawdown: 0.00% | Circuit Breaker: 🟢 OK
📍 Position: 0.011583 BTCUSDT @ $43,125.50 | Current: $44,892.30 | P&L: $20.47 (4.09%) | SL: $42,263.00 | TP: $44,850.52

🚨 Position exit triggered: Take-profit hit: $44,892.30 >= $44,850.52
🔴 Executing SELL order | 0.011583 BTCUSDT @ $44,892.30 | Reason: Take-profit hit
✅ SELL order filled | Order ID: 87654321
```

## ⚠️ Safety Checklist

Before going live with real money:

- [ ] Tested in paper mode
- [ ] Tested with Binance testnet
- [ ] Run `test_binance_connection.py` successfully
- [ ] Run `check_risk_limits.py` successfully
- [ ] Verified email notifications work
- [ ] Reviewed and understand all risk settings
- [ ] Started with small capital ($20-50)
- [ ] Set IP restrictions on Binance API
- [ ] Enabled 2FA on Binance account
- [ ] Never shared API keys with anyone

## 🔧 Troubleshooting

### Connection Issues
```
❌ Failed to connect: HTTP 401
```
**Solution:** Check API_KEY and API_SECRET in .env

### Authentication Failed
```
❌ Authentication failed
```
**Solution:** 
- Verify API has trading permissions
- Check IP whitelist on Binance
- Ensure using correct testnet/live keys

### Insufficient Balance
```
❌ Insufficient balance for order
```
**Solution:**
- Fund your account (testnet or real)
- Check funds are in Spot wallet
- Reduce MAX_POSITION_SIZE

### Circuit Breaker Triggered
```
🚨 CIRCUIT BREAKER TRIGGERED | Daily loss: -2.5% exceeds limit: -2.0%
```
**Solution:**
- This is normal - it's protecting your capital
- Will reset next trading day
- Review what caused the losses
- Consider adjusting strategy or risk limits

## 📚 Next Steps

### Phase 3: Core AI Agents (Coming Next)
- AgentX (Execution)
- HiveMind (Coordinator)
- Optima (Optimizer)
- ML-based signal generation

### Phase 4: Beautiful UI
- React dashboard
- Real-time charts
- TradingView integration
- Theme system

## 🆘 Need Help?

1. Check logs in `logs/` directory
2. Run test scripts in `scripts/`
3. Review documentation in `docs/`
4. Open GitHub issue

## ⚠️ Final Warning

**Trading involves significant risk. Only trade with money you can afford to lose.**

- Start small ($20-50)
- Use testnet first
- Monitor closely
- Scale gradually
- Never share API keys

---

**Happy Trading! 🚀**