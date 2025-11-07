@echo off
echo ========================================
echo   RoadHealth AI - Quick Setup
echo ========================================
echo.

echo [Step 1/9] Checking Python...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.11+
    pause
    exit /b 1
)
echo   Python found!
echo.

echo [Step 2/9] Creating virtual environment...
if exist venv (
    echo   Virtual environment already exists
) else (
    python -m venv venv
    echo   Virtual environment created
)
echo.

echo [Step 3/9] Activating virtual environment...
call venv\Scripts\activate.bat
echo   Activated!
echo.

echo [Step 4/9] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo   pip upgraded
echo.

echo [Step 5/9] Installing dependencies (this takes 3-5 minutes)...
echo   Please wait...
pip install -r requirements.txt
echo   Dependencies installed!
echo.

echo [Step 6/9] Creating directories...
if not exist media mkdir media
if not exist media\images mkdir media\images
if not exist media\annotated mkdir media\annotated
if not exist staticfiles mkdir staticfiles
echo   Directories created
echo.

echo [Step 7/9] Database check...
echo   IMPORTANT: Make sure PostgreSQL is installed and running!
echo   Database 'roadhealth_db' must exist!
echo.
set /p confirm="Is PostgreSQL ready? (y/n): "
if /i not "%confirm%"=="y" (
    echo.
    echo Please:
    echo   1. Install PostgreSQL
    echo   2. Create database: CREATE DATABASE roadhealth_db;
    echo   3. Run this script again
    pause
    exit /b 0
)
echo.

echo [Step 8/9] Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo   Migration failed! Check database connection.
    pause
    exit /b 1
)
echo   Migrations completed!
echo.

echo [Step 9/9] Creating superuser...
echo   Enter your admin credentials:
python manage.py createsuperuser
echo.

echo Collecting static files...
python manage.py collectstatic --noinput
echo   Static files collected!
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the server:
echo   1. venv\Scripts\activate.bat
echo   2. python manage.py runserver
echo   3. Open: http://localhost:8000
echo.
pause
