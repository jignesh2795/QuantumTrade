"""
Seed Data Script for QuantumTrade Database
Populates database with initial data for testing and development
"""

import random
import logging
from datetime import datetime, timedelta
from typing import List

from .models import Trade, Position, MarketData, StrategyResult, PerformanceMetric
from .repositories import TradeRepository, PositionRepository, MarketDataRepository, StrategyRepository, PerformanceRepository
from .connection import get_db_context

logger = logging.getLogger(__name__)

# Sample symbols for testing
SAMPLE_SYMBOLS = ["BTC-USD", "ETH-USD", "AAPL", "GOOGL", "TSLA"]

# Sample strategies
SAMPLE_STRATEGIES = ["MovingAverage", "RSI", "Breakout", "MeanReversion"]

def seed_market_data(days: int = 90) -> List[MarketData]:
    """Seed database with historical market data"""
    try:
        market_repo = MarketDataRepository()
        market_data_points = []
        
        for symbol in SAMPLE_SYMBOLS:
            base_price = random.uniform(100, 50000)
            
            for i in range(days):
                date = datetime.utcnow() - timedelta(days=days-i)
                
                # Generate realistic price movements
                open_price = base_price
                high_price = open_price * random.uniform(1.0, 1.05)
                low_price = open_price * random.uniform(0.95, 1.0)
                close_price = random.uniform(low_price, high_price)
                volume = random.uniform(1000, 1000000)
                
                market_data = MarketData(
                    symbol=symbol,
                    timestamp=date,
                    open_price=open_price,
                    high_price=high_price,
                    low_price=low_price,
                    close_price=close_price,
                    volume=volume,
                    interval="1d"
                )
                
                market_repo.add_market_data(market_data)
                market_data_points.append(market_data)
                
                # Update base price for next day
                base_price = close_price
                
        logger.info(f"Seeded {len(market_data_points)} market data points")
        return market_data_points
        
    except Exception as e:
        logger.error(f"Error seeding market data: {e}")
        return []

def seed_trades(count: int = 50) -> List[Trade]:
    """Seed database with sample trades"""
    try:
        trade_repo = TradeRepository()
        trades = []
        
        for _ in range(count):
            symbol = random.choice(SAMPLE_SYMBOLS)
            action = random.choice(["BUY", "SELL"])
            size = round(random.uniform(0.1, 10), 4)
            price = round(random.uniform(100, 50000), 2)
            strategy = random.choice(SAMPLE_STRATEGIES)
            
            trade = Trade(
                symbol=symbol,
                action=action,
                size=size,
                price=price,
                strategy_id=strategy,
                commission=round(size * price * 0.001, 2),  # 0.1% commission
                status="filled"
            )
            
            trade_repo.create_trade(trade)
            trades.append(trade)
            
        logger.info(f"Seeded {len(trades)} trades")
        return trades
        
    except Exception as e:
        logger.error(f"Error seeding trades: {e}")
        return []

def seed_positions() -> List[Position]:
    """Seed database with sample positions"""
    try:
        position_repo = PositionRepository()
        positions = []
        
        # Create a few sample positions
        sample_positions = [
            ("BTC-USD", 0.5, 45000.0),
            ("ETH-USD", 5.0, 3000.0),
            ("AAPL", 10, 150.0),
        ]
        
        for symbol, size, avg_price in sample_positions:
            position = Position(
                symbol=symbol,
                size=size,
                avg_price=avg_price,
                current_price=avg_price * random.uniform(0.95, 1.05)  # ±5% from avg
            )
            
            position_repo.create_position(position)
            positions.append(position)
            
        logger.info(f"Seeded {len(positions)} positions")
        return positions
        
    except Exception as e:
        logger.error(f"Error seeding positions: {e}")
        return []

def seed_strategy_results(count: int = 20) -> List[StrategyResult]:
    """Seed database with sample strategy results"""
    try:
        strategy_repo = StrategyRepository()
        results = []
        
        for _ in range(count):
            strategy_name = random.choice(SAMPLE_STRATEGIES)
            symbol = random.choice(SAMPLE_SYMBOLS)
            
            # Generate realistic backtest results
            initial_capital = 10000.0
            final_capital = initial_capital * random.uniform(0.8, 2.0)
            total_return = ((final_capital - initial_capital) / initial_capital) * 100
            sharpe_ratio = random.uniform(-1.0, 3.0)
            max_drawdown = random.uniform(-0.3, 0.0) * 100
            win_rate = random.uniform(0.3, 0.8) * 100
            total_trades = random.randint(50, 500)
            profitable_trades = int(total_trades * (win_rate / 100))
            
            result = StrategyResult(
                strategy_name=strategy_name,
                symbol=symbol,
                start_date=datetime.utcnow() - timedelta(days=90),
                end_date=datetime.utcnow(),
                initial_capital=initial_capital,
                final_capital=final_capital,
                total_return=round(total_return, 2),
                sharpe_ratio=round(sharpe_ratio, 2),
                max_drawdown=round(max_drawdown, 2),
                win_rate=round(win_rate, 2),
                total_trades=total_trades,
                profitable_trades=profitable_trades,
                config=f'{{"symbol": "{symbol}", "period": "1d"}}'
            )
            
            strategy_repo.save_strategy_result(result)
            results.append(result)
            
        logger.info(f"Seeded {len(results)} strategy results")
        return results
        
    except Exception as e:
        logger.error(f"Error seeding strategy results: {e}")
        return []

def seed_performance_metrics(count: int = 100) -> List[PerformanceMetric]:
    """Seed database with sample performance metrics"""
    try:
        perf_repo = PerformanceRepository()
        metrics = []
        
        metric_types = [
            "portfolio_value",
            "daily_pnl",
            "sharpe_ratio",
            "drawdown",
            "win_rate",
            "volatility"
        ]
        
        for _ in range(count):
            metric_name = random.choice(metric_types)
            
            # Generate appropriate values for each metric type
            if metric_name == "portfolio_value":
                value = random.uniform(9000, 12000)
            elif metric_name == "daily_pnl":
                value = random.uniform(-500, 500)
            elif metric_name == "sharpe_ratio":
                value = random.uniform(-1.0, 3.0)
            elif metric_name == "drawdown":
                value = random.uniform(-0.2, 0.0) * 100
            elif metric_name == "win_rate":
                value = random.uniform(40, 80)
            elif metric_name == "volatility":
                value = random.uniform(0.01, 0.1) * 100
            else:
                value = random.uniform(0, 100)
                
            metric = PerformanceMetric(
                metric_name=metric_name,
                value=value,
                timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
                context=random.choice(["daily", "weekly", "monthly", None])
            )
            
            perf_repo.save_metric(metric)
            metrics.append(metric)
            
        logger.info(f"Seeded {len(metrics)} performance metrics")
        return metrics
        
    except Exception as e:
        logger.error(f"Error seeding performance metrics: {e}")
        return []

def seed_all_data():
    """Seed all database tables with sample data"""
    try:
        logger.info("Starting database seeding...")
        
        # Seed in order of dependencies
        market_data = seed_market_data()
        trades = seed_trades()
        positions = seed_positions()
        strategy_results = seed_strategy_results()
        performance_metrics = seed_performance_metrics()
        
        logger.info("Database seeding completed successfully!")
        return {
            "market_data": len(market_data),
            "trades": len(trades),
            "positions": len(positions),
            "strategy_results": len(strategy_results),
            "performance_metrics": len(performance_metrics)
        }
        
    except Exception as e:
        logger.error(f"Error in database seeding: {e}")
        raise

if __name__ == "__main__":
    # Run seeding when script is executed directly
    seed_all_data()