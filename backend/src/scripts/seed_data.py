"""
Data seeding script for QuantumTrade backend.
Loads mock or initial data into the database.
"""

import json
from ..core.database import SessionLocal
from ..models import user, trade, strategy
from ..core.utils import parse_json_file


def seed_data():
    """Seed the database with initial data."""
    print("Seeding database with initial data...")

    db = SessionLocal()

    try:
        # Load mock strategies
        strategies_data = parse_json_file("src/mock_data/strategies.json")
        for strat_data in strategies_data:
            existing_strategy = (
                db.query(strategy.Strategy)
                .filter(strategy.Strategy.name == strat_data["name"])
                .first()
            )

            if not existing_strategy:
                new_strategy = strategy.Strategy(
                    name=strat_data["name"],
                    description=strat_data["description"],
                    parameters=strat_data["parameters"],
                    is_active=strat_data["is_active"],
                )
                db.add(new_strategy)

        # Load mock trades
        trades_data = parse_json_file("src/mock_data/sample_trades.json")
        for trade_data in trades_data:
            new_trade = trade.Trade(
                symbol=trade_data["symbol"],
                side=trade_data["side"],
                quantity=trade_data["quantity"],
                price=trade_data["price"],
            )
            db.add(new_trade)

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
