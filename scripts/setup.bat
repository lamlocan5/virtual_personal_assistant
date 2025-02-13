@echo off

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Create necessary directories
mkdir logs 2>nul
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir data\models 2>nul

REM Copy environment file if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file from example. Please update with your configurations.
)

echo Setup completed successfully!
pause