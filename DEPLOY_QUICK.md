# 🚀 Quick Deployment Guide

## ⚡ Fastest Ways to Deploy (5-10 minutes)

### 🥇 Option 1: Railway (RECOMMENDED - Easiest)

**Free tier available | PostgreSQL included | Auto-scaling**

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Add PostgreSQL in Railway dashboard
# Create superuser
railway run python manage.py createsuperuser
```

**Live URL:** `https://your-app.railway.app`

---

### 🥈 Option 2: Render (Easy - Free Tier)

**Free tier | PostgreSQL included | Auto-deploy from GitHub**

1. Push code to GitHub
2. Go to https://render.com/
3. New Web Service → Connect GitHub
4. **Build:** `pip install -r requirements.txt`
5. **Start:** `python manage.py migrate && gunicorn roadhealth.wsgi:application`
6. Add PostgreSQL database
7. Set environment variables

**Live URL:** `https://your-app.onrender.com`

---

### 🥉 Option 3: Docker (Any Server/VPS)

**Full control | Works anywhere | Requires Docker**

```powershell
# Build and run
docker-compose up -d --build

# Migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

**Local:** `http://localhost:8000`

---

## 📋 Pre-Deployment Checklist

- [ ] Generate strong SECRET_KEY:
  ```python
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Update `.env`:
  - Set `DEBUG=False`
  - Set `SECRET_KEY=<generated-key>`
  - Set `ALLOWED_HOSTS=yourdomain.com`
- [ ] Test locally first
- [ ] Push to Git repository (recommended)

---

## 🎯 Quick Deploy Commands

**Automated Deploy Script:**

```powershell
.\deploy.ps1
```

Choose your platform and follow prompts!

---

## 📚 Need More Details?

- **Full Guide:** See `DEPLOYMENT.md`
- **Setup Help:** See `SETUP_GUIDE.md`
- **Project Docs:** See `README.md`

---

## 🔐 Production Environment Variables

Copy `.env.production.example` to `.env` and fill in:

```properties
SECRET_KEY=<strong-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_NAME=roadhealth_db
DB_USER=dbuser
DB_PASSWORD=<strong-password>
DB_HOST=<your-db-host>
DB_PORT=5432
```

---

## ✅ After Deployment

1. **Create superuser:**

   ```bash
   python manage.py createsuperuser
   ```

2. **Test the app:**

   - Login at `/accounts/login/`
   - Upload test image
   - Check dashboard
   - Verify admin panel at `/admin/`

3. **Set up SSL:**

   - Railway/Render: Automatic ✓
   - Custom server: Use Let's Encrypt/Certbot

4. **Configure domain** (optional):
   - Point DNS to deployment
   - Update `ALLOWED_HOSTS`

---

## 🆘 Common Issues

**Static files not loading:**

```bash
python manage.py collectstatic --noinput
```

**Database connection error:**

- Check `.env` credentials
- Verify database exists
- Check firewall/security groups

**502 Bad Gateway:**

- Check if app is running
- Verify Gunicorn is working
- Check logs

---

## 💡 Platform Comparison

| Platform    | Free Tier  | PostgreSQL  | Auto-Deploy | Difficulty  |
| ----------- | ---------- | ----------- | ----------- | ----------- |
| **Railway** | ✅ Yes     | ✅ Included | ✅ Yes      | ⭐ Easy     |
| **Render**  | ✅ Yes     | ✅ Included | ✅ Yes      | ⭐ Easy     |
| **Heroku**  | ⚠️ Limited | ✅ Add-on   | ✅ Yes      | ⭐⭐ Medium |
| **Docker**  | N/A        | 🔧 Setup    | ❌ Manual   | ⭐⭐⭐ Hard |
| **Azure**   | 💵 Paid    | ✅ Included | ✅ Yes      | ⭐⭐⭐ Hard |

---

## 🎉 Ready to Deploy!

**Quickest path:**

1. Run `.\deploy.ps1`
2. Choose Railway (option 1)
3. Follow prompts
4. Done! 🚀

**Questions?** Check `DEPLOYMENT.md` for detailed guides!
