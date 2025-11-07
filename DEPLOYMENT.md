# 🚀 RoadHealth AI - Deployment Guide

This guide covers deploying RoadHealth AI to various cloud platforms.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deploy to Railway (Easiest - Free Tier)](#deploy-to-railway)
3. [Deploy to Render (Easy - Free Tier)](#deploy-to-render)
4. [Deploy to Heroku](#deploy-to-heroku)
5. [Deploy to Azure Web Apps](#deploy-to-azure)
6. [Deploy to AWS (EC2)](#deploy-to-aws-ec2)
7. [Deploy to DigitalOcean](#deploy-to-digitalocean)
8. [Deploy with Docker Anywhere](#deploy-with-docker)
9. [Production Configuration](#production-configuration)

---

## 📝 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ **Project files ready** (all files in `C:\Users\Hey\Desktop\project`)
- ✅ **Docker configured** (Dockerfile and docker-compose.yml exist)
- ✅ **Environment variables** (.env file configured)
- ✅ **Database choice** (PostgreSQL recommended for production)
- ✅ **Git repository** (optional but recommended)

### Update for Production

1. **Generate a strong SECRET_KEY:**

   ```python
   # In Python shell or terminal:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Update `.env` for production:**

   ```properties
   SECRET_KEY=your-generated-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. **Update `roadhealth/settings.py`:**

   ```python
   # Add to MIDDLEWARE (if not present):
   'whitenoise.middleware.WhiteNoiseMiddleware',

   # Add trusted origins for CSRF:
   CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
   ```

---

## 🚂 Deploy to Railway (Recommended - Easiest)

**Railway** offers free tier with PostgreSQL included!

### Step 1: Create Railway Account

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project"

### Step 2: Deploy from GitHub

**Option A: Deploy from GitHub (Recommended)**

1. Push your code to GitHub:

   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/roadhealth.git
   git push -u origin main
   ```

2. In Railway:
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Django!

**Option B: Deploy from Local**

1. Install Railway CLI:
   ```powershell
   npm install -g @railway/cli
   ```
2. Login and deploy:
   ```powershell
   railway login
   railway init
   railway up
   ```

### Step 3: Add PostgreSQL Database

1. In Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically connects it!

### Step 4: Configure Environment Variables

In Railway Dashboard → Variables:

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DB_NAME=${{Postgres.PGDATABASE}}
DB_USER=${{Postgres.PGUSER}}
DB_PASSWORD=${{Postgres.PGPASSWORD}}
DB_HOST=${{Postgres.PGHOST}}
DB_PORT=${{Postgres.PGPORT}}
```

### Step 5: Add Start Command

In Railway Settings → Deploy:

```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roadhealth.wsgi:application
```

### Step 6: Create Superuser

```powershell
railway run python manage.py createsuperuser
```

**Done!** Your app is live at: `https://your-app.railway.app`

---

## 🎨 Deploy to Render (Easy - Free Tier)

**Render** provides free hosting with PostgreSQL.

### Step 1: Create Render Account

1. Go to: https://render.com/
2. Sign up with GitHub

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** roadhealth-ai
   - **Environment:** Python 3
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roadhealth.wsgi:application
     ```

### Step 3: Add PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Name it and create (Free tier)
3. Copy the **Internal Database URL**

### Step 4: Environment Variables

In Web Service → Environment:

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=your-app.onrender.com
PYTHON_VERSION=3.11.0
```

### Step 5: Update settings.py for DATABASE_URL

Add this to `roadhealth/settings.py`:

```python
import dj_database_url

# Parse DATABASE_URL if available
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }
```

Install dj-database-url:

```powershell
pip install dj-database-url
# Add to requirements.txt
```

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for build (5-10 minutes)
3. Create superuser via Shell tab:
   ```bash
   python manage.py createsuperuser
   ```

**Live at:** `https://your-app.onrender.com`

---

## 💜 Deploy to Heroku

**Heroku** is a popular PaaS platform.

### Prerequisites

1. Create account: https://heroku.com/
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### Step 1: Create Heroku App

```powershell
heroku login
heroku create roadhealth-ai
```

### Step 2: Add PostgreSQL

```powershell
heroku addons:create heroku-postgresql:essential-0
```

### Step 3: Create Procfile

Create `Procfile` in project root:

```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roadhealth.wsgi:application
worker: celery -A roadhealth worker --loglevel=info
```

### Step 4: Create runtime.txt

Create `runtime.txt`:

```
python-3.11.9
```

### Step 5: Configure Environment

```powershell
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
heroku config:set DISABLE_COLLECTSTATIC=1
```

### Step 6: Deploy

```powershell
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Step 7: Run Migrations & Create Superuser

```powershell
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Step 8: Scale Dynos

```powershell
heroku ps:scale web=1
```

**Live at:** `https://roadhealth-ai.herokuapp.com`

---

## ☁️ Deploy to Azure Web Apps

**Azure** provides enterprise-grade hosting.

### Prerequisites

1. Azure account: https://azure.microsoft.com/free/
2. Install Azure CLI:
   ```powershell
   winget install Microsoft.AzureCLI
   ```

### Step 1: Login to Azure

```powershell
az login
```

### Step 2: Create Resource Group

```powershell
az group create --name RoadHealthRG --location eastus
```

### Step 3: Create PostgreSQL Server

```powershell
az postgres flexible-server create `
  --resource-group RoadHealthRG `
  --name roadhealth-db-server `
  --location eastus `
  --admin-user dbadmin `
  --admin-password "YourStrongPassword123!" `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --version 15 `
  --storage-size 32
```

### Step 4: Create Database

```powershell
az postgres flexible-server db create `
  --resource-group RoadHealthRG `
  --server-name roadhealth-db-server `
  --database-name roadhealth_db
```

### Step 5: Create Web App

```powershell
az webapp up `
  --resource-group RoadHealthRG `
  --name roadhealth-ai `
  --runtime "PYTHON:3.11" `
  --sku B1 `
  --location eastus
```

### Step 6: Configure App Settings

```powershell
az webapp config appsettings set `
  --resource-group RoadHealthRG `
  --name roadhealth-ai `
  --settings `
    SECRET_KEY="your-secret-key" `
    DEBUG=False `
    ALLOWED_HOSTS=".azurewebsites.net" `
    DB_NAME=roadhealth_db `
    DB_USER=dbadmin `
    DB_PASSWORD="YourStrongPassword123!" `
    DB_HOST=roadhealth-db-server.postgres.database.azure.com `
    DB_PORT=5432
```

### Step 7: Deploy Code

```powershell
az webapp deploy `
  --resource-group RoadHealthRG `
  --name roadhealth-ai `
  --src-path . `
  --type zip
```

### Step 8: SSH and Create Superuser

```powershell
az webapp ssh --resource-group RoadHealthRG --name roadhealth-ai
# Once in SSH:
python manage.py createsuperuser
```

**Live at:** `https://roadhealth-ai.azurewebsites.net`

---

## 🐳 Deploy with Docker Anywhere

Use Docker Compose to deploy on any server with Docker.

### Step 1: Update docker-compose.yml for Production

Create `docker-compose.prod.yml`:

```yaml
version: "3.8"

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: always

  redis:
    image: redis:7-alpine
    restart: always

  web:
    build: .
    command: gunicorn roadhealth.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  celery:
    build: .
    command: celery -A roadhealth worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Step 2: Create nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Step 3: Deploy

```bash
# On your server:
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations:
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser:
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Collect static files:
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## 🌊 Deploy to DigitalOcean

### Option 1: DigitalOcean App Platform (PaaS)

1. Create account: https://www.digitalocean.com/
2. Click "Create" → "App Platform"
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn --worker-tmp-dir /dev/shm roadhealth.wsgi:application`
5. Add PostgreSQL database from marketplace
6. Set environment variables
7. Deploy!

### Option 2: DigitalOcean Droplet (VPS)

1. Create Ubuntu 22.04 Droplet
2. SSH into droplet:
   ```bash
   ssh root@your_droplet_ip
   ```
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```
4. Install Docker Compose:
   ```bash
   apt install docker-compose
   ```
5. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/roadhealth.git
   cd roadhealth
   ```
6. Deploy with Docker Compose (see Docker section above)

---

## 🔧 Production Configuration

### Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL certificate)
- [ ] Enable CSRF protection
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable Django security middleware
- [ ] Set up database backups
- [ ] Configure logging

### Update settings.py for Production

```python
# In roadhealth/settings.py

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (use WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/app/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Performance Optimization

1. **Use a CDN** for static files (Cloudflare, AWS CloudFront)
2. **Enable caching** (Redis)
3. **Optimize database queries** (select_related, prefetch_related)
4. **Use connection pooling** (pgbouncer)
5. **Configure Gunicorn workers:**
   ```
   workers = (CPU cores × 2) + 1
   ```

### Monitoring

- Set up error tracking (Sentry)
- Monitor performance (New Relic, DataDog)
- Set up uptime monitoring (UptimeRobot)
- Enable application logging

---

## 🆘 Troubleshooting Deployment Issues

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Database Connection Error

- Verify database credentials
- Check firewall rules
- Ensure database is accessible from app

### 502 Bad Gateway

- Check if Gunicorn is running
- Verify port configuration
- Check logs: `docker-compose logs web`

### Migrations Not Running

```bash
# Run manually:
python manage.py migrate
```

---

## 🎉 Post-Deployment

After successful deployment:

1. **Create superuser account**
2. **Test all features:**
   - User registration/login
   - Image upload
   - AI analysis
   - Report generation
   - Admin panel
3. **Set up SSL certificate** (Let's Encrypt)
4. **Configure custom domain**
5. **Set up monitoring and alerts**
6. **Create database backups**
7. **Document deployment process**

---

## 📚 Additional Resources

- **Django Deployment Checklist:** https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- **Docker Best Practices:** https://docs.docker.com/develop/dev-best-practices/
- **Railway Docs:** https://docs.railway.app/
- **Render Docs:** https://render.com/docs
- **Heroku Python Guide:** https://devcenter.heroku.com/articles/getting-started-with-python

---

**Need help?** Check the platform-specific documentation or create an issue on GitHub!
