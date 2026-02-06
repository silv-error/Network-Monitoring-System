@echo off
echo ========================================
echo Network Monitor - Installation Script
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
python --version
echo.

echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully
echo.

echo [3/5] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [5/5] Setting up environment file...
if not exist .env (
    copy env.example .env
    echo Environment file created (.env)
    echo Please edit .env to configure your settings
) else (
    echo .env file already exists
)
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file if needed
echo 2. Run: python manage.py migrate
echo 3. Run: python manage.py runserver
echo 4. Open: http://127.0.0.1:8000
echo.
echo Default login:
echo   Username: admin
echo   Password: admin123
echo.
pause
