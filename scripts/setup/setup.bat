@echo off
echo 🚀 Setting up QuantumTrade Phase 1...

echo 📦 Creating virtual environment...
python -m venv venv

echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

echo 📚 Installing dependencies...
pip install -r requirements.txt

if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your settings.
)

echo 📁 Creating directories...
if not exist database mkdir database
if not exist logs mkdir logs

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your settings
echo 2. Run: python main.py
echo.
pause