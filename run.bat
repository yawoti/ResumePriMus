@echo off
echo ========================================
echo Starting Resume Transformer Backend
echo ========================================
echo.

cd backend

if not exist "..\venv\" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then install dependencies: venv\Scripts\pip install -r backend\requirements.txt
    pause
    exit /b 1
)

if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your CLAUDE_API_KEY
    echo.
)

echo Activating virtual environment...
call ..\venv\Scripts\activate

echo Starting Flask server...
python app.py
