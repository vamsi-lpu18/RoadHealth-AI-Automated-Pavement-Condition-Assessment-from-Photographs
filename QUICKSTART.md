# RoadHealth AI - Quick Start Guide

## 🚀 Quick Start (Windows)

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Git (optional)

### Step 1: Setup PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Open pgAdmin or psql command line
3. Create a new database:
   ```sql
   CREATE DATABASE roadhealth_db;
   ```

### Step 2: Run Setup Script

Open PowerShell in the project directory and run:

```powershell
.\setup.ps1
```

This script will:

- Create virtual environment
- Install all dependencies
- Create necessary directories
- Run database migrations
- Create superuser account
- Collect static files

### Step 3: Start the Server

```powershell
.\run.ps1
```

Or manually:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Step 4: Start Celery Worker (Optional)

For background image analysis, open a new terminal:

```powershell
.\venv\Scripts\Activate.ps1
celery -A roadhealth worker --loglevel=info
```

### Step 5: Access the Application

- **Main site**: http://127.0.0.1:8000
- **Admin panel**: http://127.0.0.1:8000/admin

## 📋 Default Accounts

After running setup, you'll create a superuser account. Use these credentials to log in to the admin panel.

## 🐳 Docker Setup (Alternative)

If you prefer Docker:

```powershell
# Copy environment file
copy .env.example .env

# Build and start containers
docker-compose up --build

# In a new terminal, run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

Access at: http://localhost:8000

## 📱 Using the Application

1. **Register**: Create a new account at `/accounts/register/`
2. **Login**: Sign in at `/accounts/login/`
3. **Upload**: Go to "Upload" page and select a road image
4. **Dashboard**: View analysis results and statistics
5. **Reports**: Download PDF reports or export to CSV

## 🔧 Configuration

Edit `.env` file to configure:

- Database credentials
- Email settings (for notifications)
- Google Maps API key (for map view)
- OpenAI API key (optional)

## 📚 Features

- ✅ User authentication with role-based access
- ✅ Image upload and management
- ✅ AI-powered defect detection
- ✅ Interactive dashboard with charts
- ✅ PDF report generation
- ✅ CSV data export
- ✅ Email notifications for critical conditions
- ✅ Map view with geolocation
- ✅ Responsive design with TailwindCSS

## 🆘 Troubleshooting

### Database Connection Error

- Make sure PostgreSQL is running
- Check database credentials in `.env`
- Verify database `roadhealth_db` exists

### Import Errors

- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Static Files Not Loading

- Run: `python manage.py collectstatic`
- Check `STATIC_ROOT` in settings

### Celery Not Working

- Make sure Redis is installed and running
- Windows users: Use Celery 4.x or run in WSL

## 📞 Support

For issues or questions:

- Check README.md for detailed documentation
- Review Django error messages
- Check PostgreSQL logs

## 🎉 Next Steps

1. Upload test images
2. Review AI analysis results
3. Customize AI model (replace placeholder)
4. Configure email notifications
5. Add Google Maps API key for map view
6. Deploy to production server

Happy coding! 🚀
