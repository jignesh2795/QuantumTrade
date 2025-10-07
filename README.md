# QuantumTrade - AI-Driven Trading Platform

QuantumTrade is a fully functional AI-driven trading platform with persistent database, advanced agents, backtesting capabilities, and Docker optimization.

## 🚀 Features

-   **AI Agents**: Data, Strategy, Risk, Execution, and Performance agents
-   **Persistent Database**: PostgreSQL with SQLAlchemy ORM and Supabase Cloud integration
-   **Backtesting**: Comprehensive backtesting with multiple strategies
-   **Real-time Dashboard**: Interactive frontend with live data visualization
-   **Docker Optimization**: Multi-stage builds with caching
-   **Security**: JWT authentication and authorization
-   **Monitoring**: Prometheus and Grafana integration
-   **Cloud Integration**: Supabase Cloud (Database, Auth, Real-time, Storage)

## 📁 Project Structure

```
quantumtrade/
├── backend/
│   ├── src/
│   │   ├── core/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── database/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Dockerfile.dev
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── Dockerfile.dev
├── infrastructure/
│   ├── docker-compose.yml
│   ├── postgres/
│   ├── monitoring/
│   └── ci-cd/
├── scripts/
│   ├── setup/
│   ├── backtesting/
│   └── maintenance/
└── docs/
```

## 📚 Development Stages Documentation

For detailed information about the development process, please see:

-   [Stage 1: Foundation & Core Implementation](docs/stages/stage1.md)
-   [Stage 2: Supabase Integration & Advanced Features](docs/stages/stage2.md)
-   [Stage 3: Cloud Integration with Supabase Cloud](docs/stages/stage3.md)
-   [Stage 1 & 2 Summary](docs/stages/summary.md)

## 🛠️ Quick Start

### Prerequisites

-   Docker and Docker Compose
-   Python 3.11+
-   Node.js 18+
-   Supabase Cloud Account (for Stage 3)
-   Supabase Project URL: https://jstuvjquxrciaazrsedx.supabase.co

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd quantumtrade
    ```

2. Copy and configure environment variables:

    ```bash
    cp .env.example .env
    # Edit .env with your configuration
    ```

3. Configure Supabase (if using Supabase Cloud):

    ```bash
    # For Unix/Linux/macOS
    bash scripts/configure_supabase.sh

    # For Windows
    scripts\configure_supabase.bat
    ```

    Update the `.env` file with your Supabase credentials from https://jstuvjquxrciaazrsedx.supabase.co

4. Start the application:
    ```bash
    docker-compose up --build
    ```

### Access Points

-   **Backend API**: http://localhost:8000/docs
-   **Frontend**: http://localhost:5173
-   **Database**: Supabase Cloud PostgreSQL
-   **Monitoring**: Prometheus (9090) and Grafana (3001)

## 🧪 Testing

Run backend tests:

```bash
cd backend
pytest tests/
```

## 📊 Backtesting

Run backtesting scripts:

```bash
# Run single strategy backtest
python scripts/backtesting/run_backtest.py --symbol BTC-USD --strategy moving_average

# Run multiple strategies
python scripts/backtesting/strategy_runner.py BTC-USD

# Generate report
python scripts/backtesting/report_generator.py
```

## 🧹 Maintenance

Clean up Docker cache:

```bash
./scripts/maintenance/cleanup_docker_cache.sh
```

Backup database:

```bash
./scripts/maintenance/backup_db.sh
```

## 🤖 AI Agents

-   **Data Agent**: Collects and processes market data
-   **Strategy Agent**: Generates trading signals (MA, RSI, MACD, Bollinger Bands)
-   **Risk Agent**: Manages position sizing and risk controls
-   **Execution Agent**: Simulates trade execution
-   **Performance Agent**: Tracks and analyzes performance metrics

## 📈 Monitoring

-   Prometheus metrics collection
-   Grafana dashboards for visualization
-   Custom trading metrics (PnL, Sharpe ratio, drawdown, etc.)

## 🔄 CI/CD

GitHub Actions workflow for:

-   Automated testing
-   Docker image building
-   Deployment

## 📄 Documentation

-   [Setup guides](docs/complete_setup.md)
-   [API documentation](docs/api/)
-   [Architecture diagrams](docs/architecture/)
-   [Development guidelines](docs/development/)
-   [Stage 1 & 2 documentation](docs/stages/)
-   [Stage 3.5: Supabase Auth + CI/CD](docs/stages/stage3_5.md)
-   [Stage 4: Automated Local Dev & Data Sync](docs/stages/stage4.md)
-   [Git Commit Plan](docs/git_commit_plan.md)
-   [Git Auto Commit Scripts](docs/git_auto_commit.md)
-   [Supabase Integration](docs/SUPABASE_INTEGRATION.md)
-   [Supabase Configuration](docs/SUPABASE_CONFIGURATION.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 📃 License

MIT License - see LICENSE file for details.

## 📞 Support

For support, please open an issue on GitHub.
