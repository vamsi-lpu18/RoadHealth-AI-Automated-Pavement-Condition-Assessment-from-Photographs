# RoadHealth AI - Setup and Run Script for Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RoadHealth AI - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creating necessary directories..." -ForegroundColor Yellow

$directories = @("media", "media/road_images", "media/annotated_images", "media/avatars", "static", "staticfiles", "logs", "ai_models")

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Exists: $dir" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Database Setup" -ForegroundColor Yellow
Write-Host ""
Write-Host "IMPORTANT: Make sure PostgreSQL is installed and running!" -ForegroundColor Red
Write-Host "Database name should be: roadhealth_db" -ForegroundColor Yellow
Write-Host ""
$continue = Read-Host "Have you created the PostgreSQL database 'roadhealth_db'? (y/n)"

if ($continue -ne "y") {
    Write-Host ""
    Write-Host "Please create the database first:" -ForegroundColor Yellow
    Write-Host "  1. Open PostgreSQL (pgAdmin or psql)" -ForegroundColor Cyan
    Write-Host "  2. Create database: CREATE DATABASE roadhealth_db;" -ForegroundColor Cyan
    Write-Host "  3. Re-run this script" -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creating superuser account..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Please create an admin account:" -ForegroundColor Yellow
python manage.py createsuperuser

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start Celery worker (in a new terminal), run:" -ForegroundColor Yellow
Write-Host "  celery -A roadhealth worker --loglevel=info" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then open your browser and go to:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Admin panel:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
