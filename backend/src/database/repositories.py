"""
Database Repositories for QuantumTrade Platform
Data access layer for all database operations
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func

from .connection import get_db_context
from .models import (
    Trade,
    Position,
    MarketData,
    StrategyResult,
    PerformanceMetric,
    BacktestResult,
    User,
    Configuration,
)

logger = logging.getLogger(__name__)


class BaseRepository:
    """Base repository with common database operations"""

    def __init__(self):
        pass


class TradeRepository(BaseRepository):
    """Repository for trade operations"""

    def create_trade(self, trade: Trade) -> Optional[Trade]:
        """Create a new trade"""
        try:
            with get_db_context() as db:
                db.add(trade)
                db.commit()
                db.refresh(trade)
                logger.info(
                    f"Trade created: {trade.symbol} {trade.action} {trade.size}"
                )
                return trade
        except Exception as e:
            logger.error(f"Error creating trade: {e}")
            return None

    def get_trade_by_id(self, trade_id: int) -> Optional[Trade]:
        """Get a trade by ID"""
        try:
            with get_db_context() as db:
                return db.query(Trade).filter(Trade.id == trade_id).first()
        except Exception as e:
            logger.error(f"Error getting trade {trade_id}: {e}")
            return None

    def get_trades_history(self, days: int = 30) -> List[Trade]:
        """Get trade history for the last N days"""
        try:
            with get_db_context() as db:
                start_date = datetime.utcnow() - timedelta(days=days)
                return (
                    db.query(Trade)
                    .filter(Trade.timestamp >= start_date)
                    .order_by(desc(Trade.timestamp))
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting trades history: {e}")
            return []

    def get_trades_by_symbol(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> List[Trade]:
        """Get trades for a specific symbol within a date range"""
        try:
            with get_db_context() as db:
                return (
                    db.query(Trade)
                    .filter(
                        and_(
                            Trade.symbol == symbol,
                            Trade.timestamp >= start_date,
                            Trade.timestamp <= end_date,
                        )
                    )
                    .order_by(desc(Trade.timestamp))
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting trades for {symbol}: {e}")
            return []

    def get_recent_trades(self, limit: int = 50) -> List[Trade]:
        """Get most recent trades"""
        try:
            with get_db_context() as db:
                return (
                    db.query(Trade).order_by(desc(Trade.timestamp)).limit(limit).all()
                )
        except Exception as e:
            logger.error(f"Error getting recent trades: {e}")
            return []

    def update_trade_status(self, trade_id: int, status: str) -> bool:
        """Update trade status"""
        try:
            with get_db_context() as db:
                trade = db.query(Trade).filter(Trade.id == trade_id).first()
                if trade:
                    trade.status = status
                    db.commit()
                    logger.info(f"Trade {trade_id} status updated to {status}")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error updating trade {trade_id} status: {e}")
            return False

    def delete_trade(self, trade_id: int) -> bool:
        """Delete a trade"""
        try:
            with get_db_context() as db:
                trade = db.query(Trade).filter(Trade.id == trade_id).first()
                if trade:
                    db.delete(trade)
                    db.commit()
                    logger.info(f"Trade {trade_id} deleted")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting trade {trade_id}: {e}")
            return False


class PositionRepository(BaseRepository):
    """Repository for position operations"""

    def create_position(self, position: Position) -> Optional[Position]:
        """Create a new position"""
        try:
            with get_db_context() as db:
                db.add(position)
                db.commit()
                db.refresh(position)
                logger.info(f"Position created: {position.symbol} {position.size}")
                return position
        except Exception as e:
            logger.error(f"Error creating position: {e}")
            return None

    def get_position_by_symbol(self, symbol: str) -> Optional[Position]:
        """Get a position by symbol"""
        try:
            with get_db_context() as db:
                return db.query(Position).filter(Position.symbol == symbol).first()
        except Exception as e:
            logger.error(f"Error getting position for {symbol}: {e}")
            return None

    def get_all_positions(self) -> List[Position]:
        """Get all positions"""
        try:
            with get_db_context() as db:
                return db.query(Position).all()
        except Exception as e:
            logger.error(f"Error getting all positions: {e}")
            return []

    def update_position(self, position: Position) -> Optional[Position]:
        """Update a position"""
        try:
            with get_db_context() as db:
                db.merge(position)
                db.commit()
                db.refresh(position)
                logger.info(f"Position updated: {position.symbol}")
                return position
        except Exception as e:
            logger.error(f"Error updating position {position.symbol}: {e}")
            return None

    def delete_position(self, symbol: str) -> bool:
        """Delete a position by symbol"""
        try:
            with get_db_context() as db:
                position = db.query(Position).filter(Position.symbol == symbol).first()
                if position:
                    db.delete(position)
                    db.commit()
                    logger.info(f"Position {symbol} deleted")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting position {symbol}: {e}")
            return False


class MarketDataRepository(BaseRepository):
    """Repository for market data operations"""

    def add_market_data(self, market_data: MarketData) -> Optional[MarketData]:
        """Add market data point"""
        try:
            with get_db_context() as db:
                db.add(market_data)
                db.commit()
                db.refresh(market_data)
                return market_data
        except Exception as e:
            logger.error(f"Error adding market data: {e}")
            return None

    def get_market_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> List[MarketData]:
        """Get market data for a symbol within a date range"""
        try:
            with get_db_context() as db:
                return (
                    db.query(MarketData)
                    .filter(
                        and_(
                            MarketData.symbol == symbol,
                            MarketData.timestamp >= start_date,
                            MarketData.timestamp <= end_date,
                            MarketData.interval == interval,
                        )
                    )
                    .order_by(MarketData.timestamp)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return []

    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get the latest price for a symbol"""
        try:
            with get_db_context() as db:
                latest_data = (
                    db.query(MarketData)
                    .filter(MarketData.symbol == symbol)
                    .order_by(desc(MarketData.timestamp))
                    .first()
                )

                return latest_data.close_price if latest_data else None
        except Exception as e:
            logger.error(f"Error getting latest price for {symbol}: {e}")
            return None


class StrategyRepository(BaseRepository):
    """Repository for strategy result operations"""

    def save_strategy_result(self, result: StrategyResult) -> Optional[StrategyResult]:
        """Save strategy backtest result"""
        try:
            with get_db_context() as db:
                db.add(result)
                db.commit()
                db.refresh(result)
                logger.info(
                    f"Strategy result saved: {result.strategy_name} for {result.symbol}"
                )
                return result
        except Exception as e:
            logger.error(f"Error saving strategy result: {e}")
            return None

    def get_strategy_results(self, limit: int = 50) -> List[StrategyResult]:
        """Get recent strategy results"""
        try:
            with get_db_context() as db:
                return (
                    db.query(StrategyResult)
                    .order_by(desc(StrategyResult.created_at))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting strategy results: {e}")
            return []

    def get_strategy_result_by_id(self, result_id: int) -> Optional[StrategyResult]:
        """Get strategy result by ID"""
        try:
            with get_db_context() as db:
                return (
                    db.query(StrategyResult)
                    .filter(StrategyResult.id == result_id)
                    .first()
                )
        except Exception as e:
            logger.error(f"Error getting strategy result {result_id}: {e}")
            return None


class PerformanceRepository(BaseRepository):
    """Repository for performance metric operations"""

    def save_metric(self, metric: PerformanceMetric) -> Optional[PerformanceMetric]:
        """Save performance metric"""
        try:
            with get_db_context() as db:
                db.add(metric)
                db.commit()
                db.refresh(metric)
                return metric
        except Exception as e:
            logger.error(f"Error saving performance metric: {e}")
            return None

    def get_metrics(self, metric_name: str, hours: int = 24) -> List[PerformanceMetric]:
        """Get performance metrics by name for the last N hours"""
        try:
            with get_db_context() as db:
                start_time = datetime.utcnow() - timedelta(hours=hours)
                return (
                    db.query(PerformanceMetric)
                    .filter(
                        and_(
                            PerformanceMetric.metric_name == metric_name,
                            PerformanceMetric.timestamp >= start_time,
                        )
                    )
                    .order_by(PerformanceMetric.timestamp)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting performance metrics {metric_name}: {e}")
            return []

    def get_recent_metrics(self, limit: int = 100) -> List[PerformanceMetric]:
        """Get recent performance metrics"""
        try:
            with get_db_context() as db:
                return (
                    db.query(PerformanceMetric)
                    .order_by(desc(PerformanceMetric.timestamp))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting recent metrics: {e}")
            return []


class BacktestRepository(BaseRepository):
    """Repository for backtest result operations"""

    def create_backtest_result(
        self, result: BacktestResult
    ) -> Optional[BacktestResult]:
        """Create a new backtest result"""
        try:
            with get_db_context() as db:
                db.add(result)
                db.commit()
                db.refresh(result)
                logger.info(
                    f"Backtest result created: {result.strategy} for {result.symbol}"
                )
                return result
        except Exception as e:
            logger.error(f"Error creating backtest result: {e}")
            return None

    def get_backtest_result_by_id(self, result_id: int) -> Optional[BacktestResult]:
        """Get backtest result by ID"""
        try:
            with get_db_context() as db:
                return (
                    db.query(BacktestResult)
                    .filter(BacktestResult.id == result_id)
                    .first()
                )
        except Exception as e:
            logger.error(f"Error getting backtest result {result_id}: {e}")
            return None

    def get_all_backtest_results(self, limit: int = 50) -> List[BacktestResult]:
        """Get all backtest results"""
        try:
            with get_db_context() as db:
                return (
                    db.query(BacktestResult)
                    .order_by(desc(BacktestResult.timestamp))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting backtest results: {e}")
            return []

    def get_backtest_results_by_strategy(
        self, strategy: str, limit: int = 50
    ) -> List[BacktestResult]:
        """Get backtest results by strategy"""
        try:
            with get_db_context() as db:
                return (
                    db.query(BacktestResult)
                    .filter(BacktestResult.strategy == strategy)
                    .order_by(desc(BacktestResult.timestamp))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting backtest results for strategy {strategy}: {e}")
            return []

    def get_backtest_results_by_symbol(
        self, symbol: str, limit: int = 50
    ) -> List[BacktestResult]:
        """Get backtest results by symbol"""
        try:
            with get_db_context() as db:
                return (
                    db.query(BacktestResult)
                    .filter(BacktestResult.symbol == symbol)
                    .order_by(desc(BacktestResult.timestamp))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(f"Error getting backtest results for symbol {symbol}: {e}")
            return []

    def get_backtest_results_by_strategy_and_symbol(
        self, strategy: str, symbol: str, limit: int = 50
    ) -> List[BacktestResult]:
        """Get backtest results by strategy and symbol"""
        try:
            with get_db_context() as db:
                return (
                    db.query(BacktestResult)
                    .filter(
                        and_(
                            BacktestResult.strategy == strategy,
                            BacktestResult.symbol == symbol,
                        )
                    )
                    .order_by(desc(BacktestResult.timestamp))
                    .limit(limit)
                    .all()
                )
        except Exception as e:
            logger.error(
                f"Error getting backtest results for strategy {strategy} and symbol {symbol}: {e}"
            )
            return []

    def delete_backtest_result(self, result_id: int) -> bool:
        """Delete a backtest result"""
        try:
            with get_db_context() as db:
                result = (
                    db.query(BacktestResult)
                    .filter(BacktestResult.id == result_id)
                    .first()
                )
                if result:
                    db.delete(result)
                    db.commit()
                    logger.info(f"Backtest result {result_id} deleted")
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting backtest result {result_id}: {e}")
            return False


class UserRepository(BaseRepository):
    """Repository for user operations"""

    def create_user(self, user: User) -> Optional[User]:
        """Create a new user"""
        try:
            with get_db_context() as db:
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"User created: {user.username}")
                return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(User.username == username).first()
        except Exception as e:
            logger.error(f"Error getting user {username}: {e}")
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            with get_db_context() as db:
                return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None


class ConfigurationRepository(BaseRepository):
    """Repository for configuration operations"""

    def get_config_value(self, key: str) -> Optional[str]:
        """Get configuration value by key"""
        try:
            with get_db_context() as db:
                config = (
                    db.query(Configuration).filter(Configuration.key == key).first()
                )
                return config.value if config else None
        except Exception as e:
            logger.error(f"Error getting config {key}: {e}")
            return None

    def set_config_value(self, key: str, value: str, description: str = None) -> bool:
        """Set configuration value"""
        try:
            with get_db_context() as db:
                config = (
                    db.query(Configuration).filter(Configuration.key == key).first()
                )
                if config:
                    config.value = value
                    if description:
                        config.description = description
                else:
                    config = Configuration(
                        key=key, value=value, description=description
                    )
                    db.add(config)

                db.commit()
                logger.info(f"Configuration {key} updated")
                return True
        except Exception as e:
            logger.error(f"Error setting config {key}: {e}")
            return False
