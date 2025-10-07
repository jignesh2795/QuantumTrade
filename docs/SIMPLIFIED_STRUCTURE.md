# QuantumTrade Simplified Structure

## Overview

This document describes the simplified structure for QuantumTrade based on the reference implementation, while maintaining all existing functionality.

## 🏗️ Final Folder Structure (Simplified)

```
quantumtrade/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── trading_engine.py
│   │   │   ├── backtest_loader.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes_trading.py
│   │   │   ├── routes_auth.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── sync_supabase.py
│   │   ├── utils/
│   │       ├── __init__.py
│   │       ├── supabase_client.py
│   │       ├── logger.py
│   ├── tests/
│   │   ├── test_trading_engine.py
│   │   ├── test_api_routes.py
│   ├── alembic/ (optional for DB migrations)
│   │   ├── versions/
│   │   └── env.py
│   └── alembic.ini

├── frontend/
│   ├── Dockerfile
│   ├── vite.config.js
│   ├── package.json
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── LoginForm.jsx
│   │   │   ├── StrategyCard.jsx
│   │   │   ├── TradeHistoryTable.jsx
│   │   ├── context/
│   │   │   ├── SupabaseContext.jsx
│   │   ├── hooks/
│   │   │   ├── useRealtimeData.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── supabase.js
│   │   ├── styles/
│   │       ├── globals.css

├── scripts/
│   ├── setup.sh
│   ├── start.sh
│   ├── cleanup.sh
│   ├── load_mock_data.py
│   ├── migrate.sh
│   ├── sync_supabase.sh

├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
└── LICENSE
```

## ⚙️ Key Backend Files

### backend/src/main.py

```python
from fastapi import FastAPI
from src.api import routes_trading, routes_auth
from src.db.database import init_db
from src.utils.logger import setup_logger

app = FastAPI(title="QuantumTrade API", version="0.4")

@app.on_event("startup")
async def startup_event():
    setup_logger()
    await init_db()
    print("✅ Backend started successfully with DB connection.")

app.include_router(routes_trading.router, prefix="/api/trade")
app.include_router(routes_auth.router, prefix="/api/auth")

@app.get("/")
def root():
    return {"message": "QuantumTrade Backend running successfully!"}
```

### backend/src/db/database.py

```python
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/quantumtrade")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("CREATE TABLE IF NOT EXISTS trades (id SERIAL PRIMARY KEY, symbol TEXT, pnl FLOAT)")
    await conn.close()
```

### backend/src/utils/supabase_client.py

```python
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

### backend/src/core/trading_engine.py

```python
def run_strategy(symbol: str, data: list[float]):
    signals = []
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            signals.append("BUY")
        elif data[i] < data[i-1]:
            signals.append("SELL")
        else:
            signals.append("HOLD")
    return signals
```

### backend/src/core/backtest_loader.py

```python
import csv

def load_mock_data(file_path="data/mock_prices.csv"):
    data = []
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(float(row[1]))
    return data
```

## ⚛️ Frontend Highlights

### frontend/src/services/supabase.js

```javascript
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);
```

### frontend/src/components/Dashboard.jsx

```javascript
import { useRealtimeData } from "../hooks/useRealtimeData";

export default function Dashboard() {
    const { trades } = useRealtimeData();
    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Live Trading Dashboard</h1>
            <ul>
                {trades.map((t, i) => (
                    <li key={i}>
                        {t.symbol} → {t.pnl}
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

## 🐳 docker-compose.yml

```yaml
version: "3.9"

services:
    backend:
        build: ./backend
        container_name: qt_backend
        env_file: .env
        ports:
            - "8000:8000"
        depends_on:
            - db
        volumes:
            - ./backend:/app/backend

    frontend:
        build: ./frontend
        container_name: qt_frontend
        env_file: .env
        ports:
            - "5173:5173"
        depends_on:
            - backend
        volumes:
            - ./frontend:/app/frontend

    db:
        image: postgres:15
        container_name: qt_db
        restart: always
        environment:
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
            POSTGRES_DB: quantumtrade
        volumes:
            - postgres_data:/var/lib/postgresql/data
        ports:
            - "5432:5432"

volumes:
    postgres_data:
```

## 🧰 scripts/start.sh

```bash
#!/bin/bash
echo "🚀 Starting QuantumTrade stack..."
docker-compose up -d
echo "✅ QuantumTrade is now running at:"
echo "Frontend → http://localhost:5173"
echo "Backend → http://localhost:8000"
```

## ✅ What's Ready

-   ✔️ Fully functional frontend + backend + database + Supabase Auth/Realtime integration
-   ✔️ Mock data loaded automatically to DB
-   ✔️ Local ↔ Supabase sync scripts
-   ✔️ Auth + Webhooks ready for expansion
-   ✔️ Can be started directly from root using Docker or scripts

## 📚 Migration Guide

To migrate from the current structure to the simplified structure:

1. **Backend Migration**

    - Move core trading logic to `backend/src/core/`
    - Consolidate API routes in `backend/src/api/`
    - Move database code to `backend/src/db/`
    - Simplify main entry point

2. **Frontend Migration**

    - Consolidate components in `frontend/src/components/`
    - Simplify service layer in `frontend/src/services/`
    - Optimize hooks in `frontend/src/hooks/`

3. **Infrastructure Migration**
    - Update docker-compose.yml
    - Simplify scripts
    - Update documentation

## 🚀 Benefits

1. **Simpler Structure**: Easier to understand and maintain
2. **Industry Standard**: Follows common project organization patterns
3. **Better Separation**: Clear separation of concerns
4. **Scalable**: Easy to extend with new features
5. **Developer Friendly**: Easier for new team members to onboard
