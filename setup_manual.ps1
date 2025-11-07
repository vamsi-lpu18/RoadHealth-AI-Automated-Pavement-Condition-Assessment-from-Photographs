# Simple Setup - RoadHealth AI
# Run each step manually if quick_setup.ps1 has issues

Write-Host "RoadHealth AI - Manual Setup Steps" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Copy and run these commands one by one:" -ForegroundColor Yellow
Write-Host ""

Write-Host "# Step 1: Create virtual environment" -ForegroundColor Green
Write-Host "python -m venv venv" -ForegroundColor White
Write-Host ""

Write-Host "# Step 2: Activate virtual environment" -ForegroundColor Green
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

Write-Host "# Step 3: Upgrade pip" -ForegroundColor Green
Write-Host "python -m pip install --upgrade pip" -ForegroundColor White
Write-Host ""

Write-Host "# Step 4: Install dependencies (takes 3-5 minutes)" -ForegroundColor Green
Write-Host "pip install -r requirements.txt" -ForegroundColor White
Write-Host ""

Write-Host "# Step 5: Create directories" -ForegroundColor Green
Write-Host "New-Item -ItemType Directory -Force -Path media, media\images, media\annotated, staticfiles" -ForegroundColor White
Write-Host ""

Write-Host "# Step 6: Run migrations" -ForegroundColor Green
Write-Host "python manage.py makemigrations" -ForegroundColor White
Write-Host "python manage.py migrate" -ForegroundColor White
Write-Host ""

Write-Host "# Step 7: Create superuser" -ForegroundColor Green
Write-Host "python manage.py createsuperuser" -ForegroundColor White
Write-Host ""

Write-Host "# Step 8: Collect static files" -ForegroundColor Green
Write-Host "python manage.py collectstatic --noinput" -ForegroundColor White
Write-Host ""

Write-Host "# Step 9: Start server" -ForegroundColor Green
Write-Host "python manage.py runserver" -ForegroundColor White
Write-Host ""

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Then open: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
