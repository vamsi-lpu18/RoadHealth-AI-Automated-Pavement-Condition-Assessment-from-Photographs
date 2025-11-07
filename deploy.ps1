# RoadHealth AI - Quick Deploy Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RoadHealth AI - Quick Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Choose your deployment platform:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Railway (Easiest - Free Tier)" -ForegroundColor Green
Write-Host "  2. Render (Easy - Free Tier)" -ForegroundColor Green
Write-Host "  3. Heroku" -ForegroundColor Cyan
Write-Host "  4. Docker (Any Server)" -ForegroundColor Cyan
Write-Host "  5. Exit" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📦 Deploying to Railway..." -ForegroundColor Green
        Write-Host ""
        
        # Check if Railway CLI is installed
        $railwayCli = Get-Command railway -ErrorAction SilentlyContinue
        if (-not $railwayCli) {
            Write-Host "Railway CLI not found. Installing..." -ForegroundColor Yellow
            npm install -g @railway/cli
        }
        
        Write-Host ""
        Write-Host "Step 1: Initialize Git (if not already done)" -ForegroundColor Yellow
        if (-not (Test-Path ".git")) {
            git init
            git add .
            git commit -m "Initial commit for Railway deployment"
        }
        
        Write-Host ""
        Write-Host "Step 2: Login to Railway" -ForegroundColor Yellow
        railway login
        
        Write-Host ""
        Write-Host "Step 3: Initialize Railway project" -ForegroundColor Yellow
        railway init
        
        Write-Host ""
        Write-Host "Step 4: Deploy!" -ForegroundColor Yellow
        railway up
        
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Green
        Write-Host "1. Go to Railway dashboard: https://railway.app/" -ForegroundColor Cyan
        Write-Host "2. Add PostgreSQL database (+ New → Database → PostgreSQL)" -ForegroundColor Cyan
        Write-Host "3. Set environment variables (see DEPLOYMENT.md)" -ForegroundColor Cyan
        Write-Host "4. Run: railway run python manage.py createsuperuser" -ForegroundColor Cyan
    }
    
    "2" {
        Write-Host ""
        Write-Host "🎨 Deploying to Render..." -ForegroundColor Green
        Write-Host ""
        Write-Host "Follow these steps:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "1. Push code to GitHub:" -ForegroundColor Cyan
        Write-Host "   git init" -ForegroundColor White
        Write-Host "   git add ." -ForegroundColor White
        Write-Host "   git commit -m 'Deploy to Render'" -ForegroundColor White
        Write-Host "   git push origin main" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Go to: https://render.com/" -ForegroundColor Cyan
        Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor Cyan
        Write-Host "4. Connect your GitHub repository" -ForegroundColor Cyan
        Write-Host "5. Use these settings:" -ForegroundColor Cyan
        Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor White
        Write-Host "   Start Command: python manage.py migrate && gunicorn roadhealth.wsgi:application" -ForegroundColor White
        Write-Host ""
        Write-Host "See DEPLOYMENT.md for detailed instructions!" -ForegroundColor Green
    }
    
    "3" {
        Write-Host ""
        Write-Host "💜 Deploying to Heroku..." -ForegroundColor Magenta
        Write-Host ""
        
        # Check if Heroku CLI is installed
        $herokuCli = Get-Command heroku -ErrorAction SilentlyContinue
        if (-not $herokuCli) {
            Write-Host "Heroku CLI not found!" -ForegroundColor Red
            Write-Host "Install from: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "Step 1: Login to Heroku" -ForegroundColor Yellow
        heroku login
        
        Write-Host ""
        Write-Host "Step 2: Create Heroku app" -ForegroundColor Yellow
        $appName = Read-Host "Enter app name (e.g., roadhealth-ai)"
        heroku create $appName
        
        Write-Host ""
        Write-Host "Step 3: Add PostgreSQL" -ForegroundColor Yellow
        heroku addons:create heroku-postgresql:essential-0
        
        Write-Host ""
        Write-Host "Step 4: Set environment variables" -ForegroundColor Yellow
        $secretKey = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        heroku config:set SECRET_KEY="$secretKey"
        heroku config:set DEBUG=False
        heroku config:set ALLOWED_HOSTS=".herokuapp.com"
        
        Write-Host ""
        Write-Host "Step 5: Initialize Git and deploy" -ForegroundColor Yellow
        if (-not (Test-Path ".git")) {
            git init
        }
        git add .
        git commit -m "Deploy to Heroku"
        git push heroku main
        
        Write-Host ""
        Write-Host "Step 6: Run migrations" -ForegroundColor Yellow
        heroku run python manage.py migrate
        
        Write-Host ""
        Write-Host "Step 7: Create superuser" -ForegroundColor Yellow
        heroku run python manage.py createsuperuser
        
        Write-Host ""
        Write-Host "Step 8: Scale web dyno" -ForegroundColor Yellow
        heroku ps:scale web=1
        
        Write-Host ""
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
        Write-Host "Your app is live at: https://$appName.herokuapp.com" -ForegroundColor Cyan
    }
    
    "4" {
        Write-Host ""
        Write-Host "🐳 Deploying with Docker..." -ForegroundColor Blue
        Write-Host ""
        
        # Check if Docker is installed
        $dockerCli = Get-Command docker -ErrorAction SilentlyContinue
        if (-not $dockerCli) {
            Write-Host "Docker not found!" -ForegroundColor Red
            Write-Host "Install Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "Step 1: Update .env for production" -ForegroundColor Yellow
        Write-Host "Make sure these are set in .env:" -ForegroundColor Cyan
        Write-Host "  DEBUG=False" -ForegroundColor White
        Write-Host "  SECRET_KEY=<strong-secret-key>" -ForegroundColor White
        Write-Host "  ALLOWED_HOSTS=yourdomain.com" -ForegroundColor White
        Write-Host ""
        $continue = Read-Host "Press Enter when ready to continue..."
        
        Write-Host ""
        Write-Host "Step 2: Build Docker images" -ForegroundColor Yellow
        docker-compose build
        
        Write-Host ""
        Write-Host "Step 3: Start containers" -ForegroundColor Yellow
        docker-compose up -d
        
        Write-Host ""
        Write-Host "Step 4: Run migrations" -ForegroundColor Yellow
        docker-compose exec web python manage.py migrate
        
        Write-Host ""
        Write-Host "Step 5: Create superuser" -ForegroundColor Yellow
        docker-compose exec web python manage.py createsuperuser
        
        Write-Host ""
        Write-Host "Step 6: Collect static files" -ForegroundColor Yellow
        docker-compose exec web python manage.py collectstatic --noinput
        
        Write-Host ""
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
        Write-Host "Your app is running on: http://localhost:8000" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "To deploy to a server:" -ForegroundColor Yellow
        Write-Host "1. Copy project files to server" -ForegroundColor Cyan
        Write-Host "2. Run: docker-compose up -d" -ForegroundColor Cyan
        Write-Host "3. Set up reverse proxy (Nginx) for HTTPS" -ForegroundColor Cyan
    }
    
    "5" {
        Write-Host "Exiting..." -ForegroundColor Red
        exit 0
    }
    
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📖 For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "   DEPLOYMENT.md" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Post-deployment checklist:" -ForegroundColor Yellow
Write-Host "   1. Create superuser account" -ForegroundColor White
Write-Host "   2. Test all features" -ForegroundColor White
Write-Host "   3. Set up SSL certificate" -ForegroundColor White
Write-Host "   4. Configure custom domain" -ForegroundColor White
Write-Host "   5. Set up monitoring" -ForegroundColor White
Write-Host ""
