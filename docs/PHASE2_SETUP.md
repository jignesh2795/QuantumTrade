# Phase 2: Real Trading Ready - Setup Guide

## 🎯 Phase 2 Features

✅ Real broker integration (Binance)
✅ Enhanced risk management (Guard Agent)
✅ Stop-loss and take-profit automation
✅ Daily loss limits and circuit breakers
✅ Email/SMS notifications
✅ Live trading with safeguards

## 🚀 Setup Instructions

### Step 1: Get Binance API Keys

#### For Testing (Recommended First):
1. Go to https://testnet.binance.vision/
2. Click "Generate HMAC_SHA256 Key"
3. Save your API Key and Secret Key
4. Fund your testnet account with fake USDT

#### For Live Trading:
1. Go to https://www.binance.com/en/my/settings/api-management
2. Create new API key
3. Enable "Enable Spot & Margin Trading"
4. **IMPORTANT**: Set IP restrictions for security
5. Save your API Key and Secret Key

### Step 2: Configure Environment

Edit your `.env` file:
```env
# Set to 'live' when ready for real trading
TRADING_MODE=paper

# Binance settings
EXCHANGE=binance
USE_TESTNET=true
API_KEY=your_binance_api_key_here
API_SECRET=your_binance_secret_key_here

# Risk Management
MAX_POSITION_SIZE=0.05      # Start conservative: 5%
MAX_DAILY_LOSS=0.01         # Start conservative: 1%
MAX_DRAWDOWN=0.05           # Start conservative: 5%
STOP_LOSS_PCT=0.02          # 2% stop loss
TAKE_PROFIT_PCT=0.04        # 4% take profit

# Email Notifications (Optional)
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=your_email@gmail.com

# Safety
REQUIRE_CONFIRMATION=true   # Must type YES to start live trading
DRY_RUN=false              # Set to true to simulate orders
```

### Step 3: Test with Paper Trading
```bash
# Activate environment
source venv/bin/activate

# Run in paper mode first
python main.py
```

### Step 4: Test with Binance Testnet
```bash
# Update .env
TRADING_MODE=live
USE_TESTNET=true

# Run with testnet
python main.py
```

You should see:
```
🚀 QUANTUMTRADE TRADING ENGINE - PHASE 2
Mode: LIVE
Exchange: binance
⚠️  LIVE TRADING ENABLED - Testnet
🛡️  Risk Management: ON
```

### Step 5: Go Live (When Ready)
```bash
# Update .env
TRADING_MODE=live
USE_TESTNET=false
API_KEY=your_real_api_key
API_SECRET=your_real_secret

# Start with small capital
INITIAL_CAPITAL=50

# Run
python main.py
```

You'll be prompted:
```
⚠️  LIVE TRADING MODE WARNING
==============================================================
Exchange: binance
Symbol: BTCUSDT
Max Position Size: 5.0%
Max Daily Loss: 1.0%
Stop Loss: 2.0%
==============================================================

Type 'YES' to continue with live trading: 
```

## 🛡️ Risk Management Features

### Circuit Breaker
Automatically halts trading if:
- Daily loss exceeds MAX_DAILY_LOSS
- Drawdown exceeds MAX_DRAWDOWN
- Closes all positions when triggered

### Position Sizing
- Automatically calculates safe position size
- Considers volatility
- Never exceeds MAX_POSITION_SIZE

### Stop-Loss & Take-Profit
- Automatically set on every trade
- Monitored every cycle
- Auto-closes positions when hit

### Daily Reset
- Metrics reset at start of each trading day
- Circuit breaker resets daily
- Fresh start every 24 hours

## 📧 Email Notifications

### Gmail Setup (Recommended):
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use app password in `.env`:
```env
   SMTP_PASSWORD=your_16_char_app_password
```

### Notifications You'll Receive:
- ✅ Trade executions
- ⚠️  Risk alerts (circuit breaker, limits)
- 📊 Daily summaries

## 🧪 Testing Checklist

Before going live with real money:

- [ ] Tested in paper mode
- [ ] Tested with Binance testnet
- [ ] Verified API keys work
- [ ] Confirmed email notifications work
- [ ] Reviewed risk limits
- [ ] Tested circuit breaker (set low limits)
- [ ] Tested stop-loss execution
- [ ] Started with small capital ($20-50)

## ⚠️ Safety Tips

1. **Start Small**: Begin with $20-50
2. **Use Testnet First**: Test everything on testnet
3. **Conservative Limits**: Use low risk limits initially
4. **Monitor Closely**: Watch the first few trades
5. **Enable Alerts**: Set up email/SMS notifications
6. **Set IP Restrictions**: On Binance API keys
7. **Never Share Keys**: Keep API keys secret
8. **Review Regularly**: Check logs and performance

## 📊 Expected Output
```
15:30:45 | INFO | 🚀 Starting QuantumTrade v0.2.0 (Phase 2)
15:30:45 | INFO | Mode: live
15:30:45 | INFO | 🔌 Connecting to Binance Testnet...
15:30:46 | INFO | ✅ Connected to Binance successfully
15:30:46 | INFO | ✅ Authentication successful | Account type: SPOT
15:30:46 | INFO | 🛡️  Risk Manager initialized | Max Position: 5.0%, Max Daily Loss: 1.0%
15:30:46 | INFO | 📧 Email notifications enabled
------------------------------------------------------------
📊 Market Update | BTCUSDT @ $43,125.50
💰 Balance: $50.00 | Total: $50.00 | P&L: $0.00 (0.00%)
🛡️  Risk: Daily P&L: 0.00% | Drawdown: 0.00% | Circuit Breaker: 🟢 OK
🎯 Signal: HOLD | Confidence: 0.00% | No crossover
```

## 🆘 Troubleshooting

### "Authentication failed"
- Check API key and secret
- Ensure IP whitelist includes your IP
- Verify API has trading permissions

### "Insufficient balance"
- Fund your account (testnet or real)
- Check if funds are in correct wallet (Spot)

### "Circuit breaker triggered"
- Normal safety feature
- Will reset next trading day
- Review what caused losses

### Email not sending
- Check SMTP settings
- Use app password for Gmail
- Verify firewall allows SMTP

## 📚 Next Steps

After Phase 2 is working:
- Phase 3: Add more AI agents
- Phase 4: Build beautiful UI
- Phase 5: Multi-strategy support

## ⚠️ Final Warning

**Real money is at risk. Only trade what you can afford to lose.**

Start small, test thoroughly, and scale gradually!