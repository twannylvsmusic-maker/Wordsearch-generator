@echo off
echo Starting Word Search Generator v2...
cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Python not found. Please install Python 3.8 or later.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo Starting Flask application...
echo Open your browser to: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
