# System Check Script for RoadHealth AI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RoadHealth AI - System Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([0-9]+)") {
        $minorVersion = [int]$Matches[1]
        if ($minorVersion -ge 11) {
            Write-Host "  ✓ Python $pythonVersion installed" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Python version too old. Need 3.11+" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    $allGood = $false
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version 2>&1
    if ($pgVersion) {
        Write-Host "  ✓ PostgreSQL installed: $pgVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠ PostgreSQL not found in PATH (may still be installed)" -ForegroundColor Yellow
}

# Check Redis (optional)
Write-Host "Checking Redis..." -ForegroundColor Yellow
try {
    $redisCheck = redis-cli --version 2>&1
    if ($redisCheck) {
        Write-Host "  ✓ Redis installed: $redisCheck" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠ Redis not found (optional for development)" -ForegroundColor Yellow
}

# Check Git (optional)
Write-Host "Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    if ($gitVersion) {
        Write-Host "  ✓ Git installed: $gitVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠ Git not found (optional)" -ForegroundColor Yellow
}

# Check project structure
Write-Host ""
Write-Host "Checking Project Structure..." -ForegroundColor Yellow

$requiredDirs = @(
    "roadhealth",
    "accounts",
    "core",
    "analysis",
    "reports",
    "templates"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir/" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dir/ missing!" -ForegroundColor Red
        $allGood = $false
    }
}

# Check key files
Write-Host ""
Write-Host "Checking Key Files..." -ForegroundColor Yellow

$requiredFiles = @(
    "manage.py",
    "requirements.txt",
    ".env",
    "Dockerfile",
    "docker-compose.yml"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file missing!" -ForegroundColor Red
        $allGood = $false
    }
}

# Check virtual environment
Write-Host ""
Write-Host "Checking Virtual Environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment exists" -ForegroundColor Green
    
    # Check if dependencies are installed
    if (Test-Path "venv\Lib\site-packages\django") {
        Write-Host "  ✓ Django installed in venv" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Dependencies may not be installed" -ForegroundColor Yellow
        Write-Host "    Run: .\setup.ps1" -ForegroundColor Cyan
    }
} else {
    Write-Host "  ⚠ Virtual environment not created" -ForegroundColor Yellow
    Write-Host "    Run: .\setup.ps1" -ForegroundColor Cyan
}

# Check database
Write-Host ""
Write-Host "Database Configuration:" -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env"
    $dbName = ($envContent | Select-String "DB_NAME=").ToString().Split("=")[1]
    $dbUser = ($envContent | Select-String "DB_USER=").ToString().Split("=")[1]
    
    Write-Host "  Database: $dbName" -ForegroundColor Cyan
    Write-Host "  User: $dbUser" -ForegroundColor Cyan
    Write-Host "  ⚠ Make sure PostgreSQL database '$dbName' exists!" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ All critical checks passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "  1. Ensure PostgreSQL database exists" -ForegroundColor Cyan
    Write-Host "  2. Run: .\setup.ps1" -ForegroundColor Cyan
    Write-Host "  3. Run: .\run.ps1" -ForegroundColor Cyan
} else {
    Write-Host "✗ Some checks failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install missing components before proceeding." -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
