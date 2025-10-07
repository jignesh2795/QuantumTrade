# Backtesting Engine

## 🎯 Purpose

The backtesting engine runs trading strategies deterministically on historical data to estimate performance, refine features, and train machine learning models. It provides a framework for evaluating strategy performance, optimizing parameters, and validating trading ideas before risking real capital.

## 📊 Data Format

The backtesting engine accepts CSV files with the following columns:

-   `timestamp` (ISO8601)
-   `price` (float)
-   `volume` (int) [optional]
-   `symbol` (optional if single-instrument)

Example data format:

```csv
timestamp,price,volume,symbol
2023-01-01T00:00:00Z,16500.0,125000000,BTCUSDT
2023-01-01T01:00:00Z,16600.0,130000000,BTCUSDT
2023-01-01T02:00:00Z,16750.0,115000000,BTCUSDT
```

## ⚙️ Core Components

### 1. Data Loader

Reads CSV data into pandas DataFrame (`backtest_loader.py`)

### 2. Strategy Function

Returns signal series (1 = buy, -1 = sell, 0 = hold)

### 3. Executor

Simulates orders (market orders only by default)

### 4. Performance Calculator

Calculates final P&L, drawdown, Sharpe ratio, and other metrics

## ▶️ Example Usage

```python
from src.core.backtester import run_backtest
import pandas as pd

# Load data
df = pd.read_csv('data/mock_prices.csv')

# Run backtest
results = run_backtest(df)

# View results
print(f"Final Portfolio Value: {results['final_value']}")
print(f"Total Return: {results['returns']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
```

## 🏗️ Training Flow

1. **Run Backtests**: Generate training labels (e.g., next-step up/down)
2. **Extract Features**: Calculate technical indicators (MA, RSI, returns)
3. **Train Model**: Use `model_trainer.py` to train machine learning models
4. **Evaluate**: Test on validation set and persist model artifact

## 📈 Performance Metrics

The backtesting engine calculates the following metrics:

-   **Total Return**: Overall portfolio performance
-   **Annualized Return**: Yearly performance rate
-   **Volatility**: Standard deviation of returns
-   **Sharpe Ratio**: Risk-adjusted return
-   **Sortino Ratio**: Downside risk-adjusted return
-   **Maximum Drawdown**: Largest peak-to-trough loss
-   **Calmar Ratio**: Return-to-drawdown ratio
-   **Win Rate**: Percentage of profitable trades
-   **Profit Factor**: Gross profits / gross losses
-   **Average Win/Loss**: Mean profit/loss per trade

## 🧠 Best Practices

### Time-Series Cross Validation

Use walk-forward analysis to avoid overfitting:

```python
# Example walk-forward validation
for i in range(num_windows):
    train_data = data[train_start:train_end]
    test_data = data[test_start:test_end]

    # Train model on training data
    model.fit(train_data)

    # Test on out-of-sample data
    predictions = model.predict(test_data)
```

### Avoiding Lookahead Bias

Ensure features only use past data:

```python
# Correct: Use past data only
df['returns'] = df['price'].pct_change()

# Incorrect: Using future data
df['future_returns'] = df['price'].shift(-1).pct_change()
```

### Out-of-Sample Testing

Keep a holdout dataset for final evaluation:

```python
# Split data
train_data = df[:'2022-12-31']
test_data = df['2023-01-01':]

# Train on training data
model.fit(train_data)

# Evaluate on test data
results = model.evaluate(test_data)
```

## 🛠️ Configuration

### Backtesting Parameters

Key configuration options in `.env`:

```env
# Backtesting settings
BACKTEST_DATA_PATH=./data
INITIAL_CAPITAL=100000
COMMISSION_RATE=0.001
SLIPPAGE=0.0005
```

### Strategy Parameters

Strategy-specific configuration:

```json
{
    "strategy": "moving_average_crossover",
    "parameters": {
        "fast_period": 20,
        "slow_period": 50,
        "signal_period": 9
    }
}
```

## 🧪 Testing Framework

### Unit Tests

Test individual components:

```python
def test_strategy_signal_generation():
    strategy = MovingAverageCrossover()
    data = load_test_data()
    signals = strategy.generate_signals(data)
    assert len(signals) == len(data)
    assert all(signal in [-1, 0, 1] for signal in signals)
```

### Integration Tests

Test component interactions:

```python
def test_full_backtest_run():
    engine = BacktestingEngine()
    strategy = TestStrategy()
    data = load_sample_data()
    results = engine.run(strategy, data)
    assert results.total_return > 0
    assert len(results.trades) > 0
```

### Performance Tests

Ensure efficient execution:

```python
def test_backtest_performance():
    engine = BacktestingEngine()
    data = load_large_dataset()
    start_time = time.time()
    engine.run(strategy, data)
    end_time = time.time()
    assert (end_time - start_time) < 30  # Should complete in 30 seconds
```

## 🚀 Running Backtests

### Command Line Interface

Run backtests from the command line:

```bash
# Basic backtest
python -m backtesting.runner --strategy moving_average --symbol AAPL --days 365

# With parameter optimization
python -m backtesting.runner --strategy rsi --symbol BTCUSD --optimize --period 14

# Live backtesting
python -m backtesting.runner --strategy momentum --live --exchange binance
```

### Programmatic Interface

Run backtests programmatically:

```python
from backtesting import BacktestingEngine
from strategies import MovingAverageCrossover

engine = BacktestingEngine(initial_capital=100000)
strategy = MovingAverageCrossover(fast_period=20, slow_period=50)
data = load_historical_data("AAPL", days=365)

results = engine.run(strategy, data)
print(f"Total Return: {results.total_return:.2%}")
print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
```

## 📊 Results Analysis

### Visualization Tools

Interactive charts and graphs:

-   **Equity Curve**: Portfolio value over time
-   **Drawdown Chart**: Visualize maximum drawdown periods
-   **Trade Distribution**: Histogram of trade returns
-   **Monthly Returns**: Heatmap of monthly performance
-   **Underwater Chart**: Cumulative drawdown over time

### Performance Reporting

Generate comprehensive strategy reports:

-   **Equity Curve**: Visualize portfolio value over time
-   **Drawdown Chart**: Show maximum drawdown periods
-   **Trade Analysis**: Detailed breakdown of individual trades
-   **Metrics Summary**: Key performance indicators

## 🔒 Risk Management

### Position Sizing

Dynamic position sizing based on:

-   **Fixed Fraction**: Constant percentage of portfolio
-   **Kelly Criterion**: Optimal bet sizing formula
-   **Volatility Adjusted**: Adjust for asset volatility
-   **Account Curve**: Scale with account growth

### Stop Losses and Take Profits

Automated risk controls:

-   **Fixed Dollar**: Set dollar amount stop loss
-   **Percentage**: Set percentage stop loss
-   **Volatility**: Set stop based on ATR
-   **Trailing**: Dynamic stop that follows price

### Portfolio-Level Risk

Manage overall portfolio risk:

-   **Correlation Analysis**: Monitor position correlations
-   **Sector Exposure**: Limit exposure to single sectors
-   **Market Beta**: Adjust for market direction
-   **Value at Risk**: Statistical risk measure

## 🔄 Continuous Improvement

### Strategy Monitoring

Track strategy performance over time:

-   **Performance Decay**: Monitor declining returns
-   **Market Regime Changes**: Adapt to changing markets
-   **Parameter Drift**: Track optimal parameter changes
-   **Capacity Constraints**: Monitor strategy capacity

### Automated Optimization

Continuous strategy improvement:

-   **Online Learning**: Update models with new data
-   **Adaptive Parameters**: Automatically adjust parameters
-   **Regime Detection**: Switch strategies based on market conditions
-   **Ensemble Methods**: Combine multiple strategies dynamically

## 📚 Additional Resources

-   [Backtesting Best Practices](https://www.investopedia.com/articles/trading/07/backtesting.asp)
-   [Common Backtesting Mistakes](https://www.quantstart.com/articles/Common-Backtesting-Mistakes/)
-   [Performance Metrics Guide](https://www.investopedia.com/terms/s/sharperatio.asp)
