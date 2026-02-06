@echo off
echo ========================================
echo Network Monitor - Starting Server
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)
echo.

echo Starting Django development server...
echo.
echo Dashboard will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
