# 🚀 RoadHealth AI - Step-by-Step Setup Guide

Choose your preferred setup method:

- **Option A: Local Development** (Recommended for development)
- **Option B: Docker** (Easier, but requires Docker Desktop)

---

## ✅ Prerequisites Check

Before starting, make sure you have:

- ✅ Python 3.11+ (You have: 3.13.9 ✓)
- ✅ PostgreSQL 12+ installed
- ✅ Git (optional)

---

## 🎯 Option A: Local Development Setup (Recommended)

### Step 1: Install PostgreSQL

1. **Download PostgreSQL** from: https://www.postgresql.org/download/windows/
2. **Run the installer** and remember your password
3. **Open pgAdmin 4** (installed with PostgreSQL)

### Step 2: Create Database

Open **PowerShell** or **SQL Shell (psql)** and run:

```powershell
# Connect to PostgreSQL
psql -U postgres

# Then in psql, create the database:
CREATE DATABASE roadhealth_db;

# Create a user (optional - or use 'postgres')
CREATE USER roadhealth_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE roadhealth_db TO roadhealth_user;

# Exit psql
\q
```

**OR** use pgAdmin 4:

1. Right-click on "Databases" → "Create" → "Database"
2. Database name: `roadhealth_db`
3. Click "Save"

### Step 3: Configure Environment Variables

Edit the `.env` file in your project folder:

```properties
# Update these if you changed database credentials
DB_NAME=roadhealth_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 4: Create Virtual Environment

Open PowerShell in the project folder:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 5: Install Dependencies

```powershell
# Make sure venv is activated (you should see (venv) in your prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

This will take a few minutes...

### Step 6: Run Migrations

```powershell
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Admin User

```powershell
# Create superuser account
python manage.py createsuperuser

# Enter:
# - Username (e.g., admin)
# - Email (e.g., admin@example.com)
# - Password (min 8 characters)
```

### Step 8: Create Required Directories

```powershell
# Create media directories
New-Item -ItemType Directory -Force -Path media, media\images, media\annotated, staticfiles
```

### Step 9: Collect Static Files

```powershell
python manage.py collectstatic --noinput
```

### Step 10: Run the Development Server

```powershell
python manage.py runserver
```

**🎉 Success!** Open your browser to: **http://localhost:8000**

### Step 11: (Optional) Run Celery for Async Tasks

Open a **NEW PowerShell window**, navigate to project folder, activate venv, and run:

```powershell
cd C:\Users\Hey\Desktop\project
.\venv\Scripts\Activate.ps1

# Install Redis (for Windows, use WSL or download from:)
# https://github.com/microsoftarchive/redis/releases

# Run Celery worker
celery -A roadhealth worker --loglevel=info --pool=solo
```

**Note:** Celery on Windows requires `--pool=solo` flag.

---

## 🐳 Option B: Docker Setup

### Prerequisites

- Install **Docker Desktop** from: https://www.docker.com/products/docker-desktop/
- Make sure Docker is running

### Step 1: Update Environment for Docker

Edit `.env` file - change DB_HOST:

```properties
DB_HOST=db  # Change from 'localhost' to 'db'
```

### Step 2: Build and Run with Docker Compose

```powershell
# Build and start all services
docker-compose up -d --build

# Wait for services to start (30-60 seconds)
Start-Sleep -Seconds 30

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Step 3: Access the Application

**🎉 Success!** Open your browser to: **http://localhost:8000**

### Docker Commands Reference

```powershell
# View logs
docker-compose logs -f web

# Stop all services
docker-compose down

# Restart services
docker-compose restart

# Remove everything (including database!)
docker-compose down -v
```

---

## 🧪 Testing Your Installation

### 1. Login Test

1. Go to: http://localhost:8000/accounts/login/
2. Login with your superuser credentials
3. You should see the dashboard

### 2. Upload Test

1. Click "Upload Image" in navigation
2. Upload a road/pavement image
3. Add details and submit
4. Check if image appears in "My Images"

### 3. Dashboard Test

1. Go to Dashboard
2. You should see statistics and charts
3. Try filter options

### 4. Admin Panel Test

1. Go to: http://localhost:8000/admin/
2. Login with superuser
3. Explore the admin interface

### 5. API Test

```powershell
# Get JWT token
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{\"username\":\"admin\",\"password\":\"your_password\"}'

# Use token to access API
curl http://localhost:8000/api/images/ -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔧 Troubleshooting

### Problem: "django.db.utils.OperationalError: could not connect to server"

**Solution:** PostgreSQL is not running or wrong credentials in `.env`

```powershell
# Check if PostgreSQL is running:
Get-Service -Name postgresql*
```

### Problem: "No module named 'django'"

**Solution:** Virtual environment not activated or dependencies not installed

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problem: "TemplateDoesNotExist"

**Solution:** Run collectstatic

```powershell
python manage.py collectstatic --noinput
```

### Problem: Port 8000 already in use

**Solution:** Kill the process or use different port

```powershell
# Use different port
python manage.py runserver 8080

# Or find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Problem: Celery not working on Windows

**Solution:** Use the `--pool=solo` flag

```powershell
celery -A roadhealth worker --loglevel=info --pool=solo
```

---

## 📱 Next Steps After Setup

1. **Customize Settings**

   - Edit `roadhealth/settings.py` for production settings
   - Configure email in `.env` for notifications
   - Add Google Maps API key for map features

2. **Replace AI Model**

   - The current AI model is a placeholder
   - Replace `analysis/ai_model.py` with your trained model
   - Update `detect_defects()` method

3. **Add Test Data**

   - Upload sample road images
   - Test different defect types
   - Generate reports

4. **Deploy to Production**
   - See `README.md` for deployment guide
   - Use PostgreSQL in production (not SQLite)
   - Set `DEBUG=False` in production
   - Use proper SECRET_KEY

---

## 🆘 Need Help?

- Check `README.md` for full documentation
- Check `TESTING.md` for testing guidelines
- Check `PROJECT_SUMMARY.md` for technical details

---

**Ready to start? Follow Option A (Local) or Option B (Docker) above!** 🚀
