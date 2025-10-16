# QuantumTrade

QuantumTrade is an algorithmic trading platform designed for both beginners and experienced traders. It provides a comprehensive environment for developing, testing, and executing trading strategies with a focus on risk management and performance optimization.

## Features

- **Paper Trading**: Simulate trading strategies without risking real capital
- **Multiple Strategies**: Implement and test various trading algorithms
- **Risk Management**: Built-in position sizing and loss limiting
- **Performance Tracking**: Monitor strategy performance with detailed metrics
- **Modular Architecture**: Extensible design for adding new features

## Project Structure

```
QuantumTrade/
├── .github/               # GitHub workflows and configurations
├── backend/               # Core trading engine
│   ├── core/              # Main trading components
│   ├── strategies/        # Trading strategies
│   ├── db/                # Database models and utilities
│   ├── api/               # API endpoints and routes
│   ├── ai_agents/         # AI-powered trading agents
│   ├── learning_mode/     # Educational components
│   ├── analytics/         # Performance and risk analytics
│   ├── utils/             # Helper functions
│   └── tests/             # Unit and integration tests
├── frontend/              # Web interface (React)
├── config/                # Configuration files
├── database/              # Database files (excluded from git)
├── logs/                  # Log files (excluded from git)
├── docs/                  # Documentation
├── plugins/               # Extension plugins
├── scripts/               # Utility scripts
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── environment.yml        # Conda environment definition
├── requirements.txt       # Pip dependencies
├── main.py               # Application entry point
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Conda (recommended) or pip
- Git

### Option 1: Using Conda (Recommended)

1. Install Miniconda or Anaconda if you haven't already:
   ```bash
   # Download from: https://docs.conda.io/en/latest/miniconda.html
   ```

2. Create and activate the conda environment:
   ```bash
   conda env create -f environment.yml
   conda activate quantumtrade
   ```

### Option 2: Using pip

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings (API keys, trading parameters, etc.)

3. Create necessary directories:
   ```bash
   mkdir database logs
   ```

## Usage

Run the main application:
```bash
python main.py
```

The application will start in paper trading mode by default, simulating trades without using real money.

## Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest backend/tests/unit/test_engine.py

# Run tests with coverage
python -m pytest --cov=backend --cov-report=html
```

### Code Formatting

```bash
# Format code with black
black .

# Check code style with ruff
ruff check .

# Fix code style issues with ruff
ruff check . --fix
```

## Git Workflow

This repository uses a `.gitignore` file to exclude unnecessary files from version control:

### Excluded Files and Directories

- Virtual environments (`venv/`, `.venv/`)
- Log files (`logs/`)
- Database files (`database/*.db`)
- Environment files (`.env`)
- Cache directories (`__pycache__/`)
- IDE-specific files (`.vscode/`, `.idea/`)
- Compiled Python files (`*.pyc`, `*.pyo`, `*.pyd`)

### Best Practices

1. Never commit sensitive information (API keys, passwords)
2. Use feature branches for new development
3. Keep commits small and focused
4. Write descriptive commit messages
5. Run tests before pushing changes

## Configuration

Key environment variables:
- `TRADING_MODE`: Set to "paper" for simulation or "live" for real trading (Phase 2)
- `EXCHANGE`: Target exchange (e.g., "binance")
- `DEFAULT_SYMBOL`: Trading pair (e.g., "BTCUSDT")
- `INITIAL_CAPITAL`: Starting capital for paper trading
- `STRATEGY`: Trading strategy to use

## Troubleshooting

### Common Issues

1. **TA-Lib Installation Issues**:
   - Windows: Download pre-compiled wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
   - macOS: Install via Homebrew: `brew install ta-lib`
   - Linux: Compile from source

2. **Permission Errors**:
   - Run commands with appropriate privileges
   - Check file and directory permissions

3. **Dependency Conflicts**:
   - Use conda environment for better dependency management
   - Update dependencies regularly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.