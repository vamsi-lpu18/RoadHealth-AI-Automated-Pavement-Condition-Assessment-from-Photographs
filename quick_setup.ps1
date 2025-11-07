# RoadHealth AI - Quick Setup Script
# This script automates the local development setup

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RoadHealth AI - Quick Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running from project directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: Please run this script from the project directory!" -ForegroundColor Red
    exit 1
}

# Step 1: Check Python
Write-Host "[Step 1/9] Checking Python..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
Write-Host "  Found: $pythonCheck" -ForegroundColor Green

# Step 2: Create Virtual Environment
Write-Host ""
Write-Host "[Step 2/9] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  Virtual environment created" -ForegroundColor Green
}

# Step 3: Activate Virtual Environment
Write-Host ""
Write-Host "[Step 3/9] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  Virtual environment activated" -ForegroundColor Green

# Step 4: Upgrade pip
Write-Host ""
Write-Host "[Step 4/9] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "  pip upgraded" -ForegroundColor Green

# Step 5: Install Dependencies
Write-Host ""
Write-Host "[Step 5/9] Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
Write-Host "  This may take 3-5 minutes. Please wait..." -ForegroundColor Cyan
pip install -r requirements.txt --quiet
Write-Host "  Dependencies installed" -ForegroundColor Green

# Step 6: Create Directories
Write-Host ""
Write-Host "[Step 6/9] Creating required directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "media", "media\images", "media\annotated", "staticfiles" | Out-Null
Write-Host "  Directories created" -ForegroundColor Green

# Step 7: Check Database Configuration
Write-Host ""
Write-Host "[Step 7/9] Checking database configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $dbNameLine = $envContent | Select-String "DB_NAME="
    if ($dbNameLine) {
        $dbName = $dbNameLine.ToString().Split("=")[1].Trim()
        Write-Host "  Database name: $dbName" -ForegroundColor Cyan
    }
    Write-Host ""
    Write-Host "  IMPORTANT: Make sure PostgreSQL is installed and running!" -ForegroundColor Yellow
    Write-Host "  Database must exist in PostgreSQL!" -ForegroundColor Yellow
    Write-Host ""
    
    $response = Read-Host "  Is PostgreSQL running and database created? (y/n)"
    if ($response -ne "y") {
        Write-Host ""
        Write-Host "  Please complete these steps:" -ForegroundColor Yellow
        Write-Host "  1. Install PostgreSQL from: https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
        Write-Host "  2. Open pgAdmin 4 or psql" -ForegroundColor Cyan
        Write-Host "  3. Create database: CREATE DATABASE roadhealth_db;" -ForegroundColor Cyan
        Write-Host "  4. Run this script again" -ForegroundColor Cyan
        Write-Host ""
        exit 0
    }
} else {
    Write-Host "  .env file not found!" -ForegroundColor Red
    exit 1
}

# Step 8: Run Migrations
Write-Host ""
Write-Host "[Step 8/9] Running database migrations..." -ForegroundColor Yellow
Write-Host "  Creating migrations..." -ForegroundColor Cyan
python manage.py makemigrations
Write-Host "  Applying migrations..." -ForegroundColor Cyan
python manage.py migrate

# Step 9: Create Superuser
Write-Host ""
Write-Host "[Step 9/9] Creating superuser account..." -ForegroundColor Yellow
Write-Host "  Please enter your admin credentials:" -ForegroundColor Cyan
python manage.py createsuperuser

# Collect Static Files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Success Message
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Activate virtual environment:" -ForegroundColor Cyan
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "  2. Run the server:" -ForegroundColor Cyan
Write-Host "     python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "  3. Open your browser:" -ForegroundColor Cyan
Write-Host "     http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "For Celery (optional - async tasks):" -ForegroundColor Yellow
Write-Host "  celery -A roadhealth worker --loglevel=info --pool=solo" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - SETUP_GUIDE.md - Step-by-step guide" -ForegroundColor White
Write-Host "  - README.md - Full documentation" -ForegroundColor White
Write-Host "  - TESTING.md - Testing guide" -ForegroundColor White
Write-Host ""
