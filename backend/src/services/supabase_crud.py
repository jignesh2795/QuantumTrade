"""
Supabase CRUD Operations for QuantumTrade Platform
Data access layer for database operations using direct PostgreSQL access
"""

import logging
from typing import List, Dict, Any, Optional
from .supabase_client import get_supabase_client
from .supabase_models import (
    User,
    Trade,
    Portfolio,
    StrategyExecution,
    StrategyConfiguration,
)
from sqlalchemy import text
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class SupabaseCRUD:
    """CRUD operations for database using direct PostgreSQL access"""

    @staticmethod
    def create_trade(
        user_id: str, asset: str, trade_type: str, amount: float, price: float
    ) -> Optional[Dict]:
        """
        Create a new trade record

        Args:
            user_id: User ID
            asset: Asset symbol (e.g., BTC-USD)
            trade_type: BUY or SELL
            amount: Trade amount
            price: Trade price

        Returns:
            Created trade record or None if failed
        """
        try:
            db = get_supabase_client()
            trade_id = str(uuid.uuid4())
            timestamp = datetime.utcnow()

            # Insert trade record
            query = text(
                """
                INSERT INTO trades (id, user_id, asset, trade_type, amount, price, timestamp)
                VALUES (:id, :user_id, :asset, :trade_type, :amount, :price, :timestamp)
                RETURNING *
            """
            )

            result = db.execute(
                query,
                {
                    "id": trade_id,
                    "user_id": user_id,
                    "asset": asset,
                    "trade_type": trade_type,
                    "amount": amount,
                    "price": price,
                    "timestamp": timestamp,
                },
            )

            db.commit()
            trade_record = result.fetchone()

            if trade_record:
                logger.info(f"Trade created: {asset} {trade_type} {amount}@{price}")
                # Convert to dictionary
                return {
                    "id": trade_record[0],
                    "user_id": trade_record[1],
                    "asset": trade_record[2],
                    "trade_type": trade_record[3],
                    "amount": float(trade_record[4]),
                    "price": float(trade_record[5]),
                    "timestamp": (
                        trade_record[6].isoformat() if trade_record[6] else None
                    ),
                }
            return None
        except Exception as e:
            logger.error(f"Error creating trade: {e}")
            if "db" in locals():
                db.rollback()
            return None
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def get_trades(user_id: str, limit: int = 100) -> List[Dict]:
        """
        Get trades for a user

        Args:
            user_id: User ID
            limit: Maximum number of trades to retrieve

        Returns:
            List of trade records
        """
        try:
            db = get_supabase_client()

            query = text(
                """
                SELECT id, user_id, asset, trade_type, amount, price, timestamp
                FROM trades
                WHERE user_id = :user_id
                ORDER BY timestamp DESC
                LIMIT :limit
            """
            )

            result = db.execute(query, {"user_id": user_id, "limit": limit})
            trades = result.fetchall()

            # Convert to list of dictionaries
            return [
                {
                    "id": trade[0],
                    "user_id": trade[1],
                    "asset": trade[2],
                    "trade_type": trade[3],
                    "amount": float(trade[4]),
                    "price": float(trade[5]),
                    "timestamp": trade[6].isoformat() if trade[6] else None,
                }
                for trade in trades
            ]
        except Exception as e:
            logger.error(f"Error getting trades: {e}")
            return []
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def get_portfolio(user_id: str) -> List[Dict]:
        """
        Get portfolio for a user

        Args:
            user_id: User ID

        Returns:
            List of portfolio records
        """
        try:
            db = get_supabase_client()

            query = text(
                """
                SELECT id, user_id, asset, quantity, avg_price
                FROM portfolio
                WHERE user_id = :user_id
            """
            )

            result = db.execute(query, {"user_id": user_id})
            portfolio_items = result.fetchall()

            # Convert to list of dictionaries
            return [
                {
                    "id": item[0],
                    "user_id": item[1],
                    "asset": item[2],
                    "quantity": float(item[3]),
                    "avg_price": float(item[4]),
                }
                for item in portfolio_items
            ]
        except Exception as e:
            logger.error(f"Error getting portfolio: {e}")
            return []
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def update_portfolio(
        user_id: str, asset: str, quantity: float, avg_price: float
    ) -> Optional[Dict]:
        """
        Update portfolio record for a user

        Args:
            user_id: User ID
            asset: Asset symbol
            quantity: Asset quantity
            avg_price: Average price

        Returns:
            Updated portfolio record or None if failed
        """
        try:
            db = get_supabase_client()

            # First, try to update existing record
            query = text(
                """
                UPDATE portfolio
                SET quantity = :quantity, avg_price = :avg_price
                WHERE user_id = :user_id AND asset = :asset
                RETURNING id, user_id, asset, quantity, avg_price
            """
            )

            result = db.execute(
                query,
                {
                    "user_id": user_id,
                    "asset": asset,
                    "quantity": quantity,
                    "avg_price": avg_price,
                },
            )

            updated_record = result.fetchone()

            # If no record was updated, create a new one
            if not updated_record:
                portfolio_id = str(uuid.uuid4())
                query = text(
                    """
                    INSERT INTO portfolio (id, user_id, asset, quantity, avg_price)
                    VALUES (:id, :user_id, :asset, :quantity, :avg_price)
                    RETURNING id, user_id, asset, quantity, avg_price
                """
                )

                result = db.execute(
                    query,
                    {
                        "id": portfolio_id,
                        "user_id": user_id,
                        "asset": asset,
                        "quantity": quantity,
                        "avg_price": avg_price,
                    },
                )

                updated_record = result.fetchone()

            db.commit()

            if updated_record:
                return {
                    "id": updated_record[0],
                    "user_id": updated_record[1],
                    "asset": updated_record[2],
                    "quantity": float(updated_record[3]),
                    "avg_price": float(updated_record[4]),
                }
            return None
        except Exception as e:
            logger.error(f"Error updating portfolio: {e}")
            if "db" in locals():
                db.rollback()
            return None
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def create_strategy_execution(
        user_id: str, strategy_name: str, asset: str, signal: str, confidence: float
    ) -> Optional[Dict]:
        """
        Create a strategy execution record

        Args:
            user_id: User ID
            strategy_name: Strategy name
            asset: Asset symbol
            signal: BUY, SELL, or HOLD
            confidence: Confidence level (0.0 - 1.0)

        Returns:
            Created strategy execution record or None if failed
        """
        try:
            db = get_supabase_client()
            execution_id = str(uuid.uuid4())
            executed_at = datetime.utcnow()

            query = text(
                """
                INSERT INTO strategy_executions 
                (id, user_id, strategy_name, asset, signal, confidence, executed_at)
                VALUES (:id, :user_id, :strategy_name, :asset, :signal, :confidence, :executed_at)
                RETURNING id, user_id, strategy_name, asset, signal, confidence, executed_at
            """
            )

            result = db.execute(
                query,
                {
                    "id": execution_id,
                    "user_id": user_id,
                    "strategy_name": strategy_name,
                    "asset": asset,
                    "signal": signal,
                    "confidence": confidence,
                    "executed_at": executed_at,
                },
            )

            db.commit()
            execution_record = result.fetchone()

            if execution_record:
                logger.info(
                    f"Strategy execution created: {strategy_name} {asset} {signal}"
                )
                return {
                    "id": execution_record[0],
                    "user_id": execution_record[1],
                    "strategy_name": execution_record[2],
                    "asset": execution_record[3],
                    "signal": execution_record[4],
                    "confidence": float(execution_record[5]),
                    "executed_at": (
                        execution_record[6].isoformat() if execution_record[6] else None
                    ),
                }
            return None
        except Exception as e:
            logger.error(f"Error creating strategy execution: {e}")
            if "db" in locals():
                db.rollback()
            return None
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def get_strategy_configurations(user_id: str) -> List[Dict]:
        """
        Get strategy configurations for a user

        Args:
            user_id: User ID

        Returns:
            List of strategy configuration records
        """
        try:
            db = get_supabase_client()

            query = text(
                """
                SELECT id, user_id, strategy_name, asset, is_active, config, created_at, updated_at
                FROM strategy_configurations
                WHERE user_id = :user_id
            """
            )

            result = db.execute(query, {"user_id": user_id})
            configs = result.fetchall()

            # Convert to list of dictionaries
            return [
                {
                    "id": config[0],
                    "user_id": config[1],
                    "strategy_name": config[2],
                    "asset": config[3],
                    "is_active": config[4],
                    "config": config[5],
                    "created_at": config[6].isoformat() if config[6] else None,
                    "updated_at": config[7].isoformat() if config[7] else None,
                }
                for config in configs
            ]
        except Exception as e:
            logger.error(f"Error getting strategy configurations: {e}")
            return []
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def update_strategy_configuration(
        user_id: str, strategy_name: str, asset: str, is_active: bool, config: Dict
    ) -> Optional[Dict]:
        """
        Update strategy configuration

        Args:
            user_id: User ID
            strategy_name: Strategy name
            asset: Asset symbol
            is_active: Whether strategy is active
            config: Configuration data

        Returns:
            Updated strategy configuration record or None if failed
        """
        try:
            db = get_supabase_client()

            # First, try to update existing record
            query = text(
                """
                UPDATE strategy_configurations
                SET is_active = :is_active, config = :config, updated_at = :updated_at
                WHERE user_id = :user_id AND strategy_name = :strategy_name AND asset = :asset
                RETURNING id, user_id, strategy_name, asset, is_active, config, created_at, updated_at
            """
            )

            result = db.execute(
                query,
                {
                    "user_id": user_id,
                    "strategy_name": strategy_name,
                    "asset": asset,
                    "is_active": is_active,
                    "config": config,
                    "updated_at": datetime.utcnow(),
                },
            )

            updated_record = result.fetchone()

            # If no record was updated, create a new one
            if not updated_record:
                config_id = str(uuid.uuid4())
                query = text(
                    """
                    INSERT INTO strategy_configurations 
                    (id, user_id, strategy_name, asset, is_active, config, created_at, updated_at)
                    VALUES (:id, :user_id, :strategy_name, :asset, :is_active, :config, :created_at, :updated_at)
                    RETURNING id, user_id, strategy_name, asset, is_active, config, created_at, updated_at
                """
                )

                result = db.execute(
                    query,
                    {
                        "id": config_id,
                        "user_id": user_id,
                        "strategy_name": strategy_name,
                        "asset": asset,
                        "is_active": is_active,
                        "config": config,
                        "created_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    },
                )

                updated_record = result.fetchone()

            db.commit()

            if updated_record:
                return {
                    "id": updated_record[0],
                    "user_id": updated_record[1],
                    "strategy_name": updated_record[2],
                    "asset": updated_record[3],
                    "is_active": updated_record[4],
                    "config": updated_record[5],
                    "created_at": (
                        updated_record[6].isoformat() if updated_record[6] else None
                    ),
                    "updated_at": (
                        updated_record[7].isoformat() if updated_record[7] else None
                    ),
                }
            return None
        except Exception as e:
            logger.error(f"Error updating strategy configuration: {e}")
            if "db" in locals():
                db.rollback()
            return None
        finally:
            if "db" in locals():
                db.close()

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[Dict]:
        """
        Authenticate user (simplified for local development)

        Args:
            email: User email
            password: User password

        Returns:
            User record if authenticated, None otherwise
        """
        try:
            db = get_supabase_client()

            query = text(
                """
                SELECT id, email, password_hash, created_at
                FROM users
                WHERE email = :email
            """
            )

            result = db.execute(query, {"email": email})
            user_record = result.fetchone()

            if user_record:
                # In a real implementation, you would verify the password
                # This is a simplified version for local development
                return {
                    "id": user_record[0],
                    "email": user_record[1],
                    "password_hash": user_record[2],
                    "created_at": (
                        user_record[3].isoformat() if user_record[3] else None
                    ),
                }
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
        finally:
            if "db" in locals():
                db.close()
