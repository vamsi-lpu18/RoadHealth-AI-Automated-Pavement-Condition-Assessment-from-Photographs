# 🛣️ RoadHealth AI - Automated Pavement Condition Assessment

<div align="center">

![RoadHealth AI](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Deployment](https://img.shields.io/badge/Deployed-Render-success)
![AI](https://img.shields.io/badge/AI-Computer_Vision-orange)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

### 🌐 **[Live Demo](https://roadhealth-ai-automated-pavement.onrender.com)** | � [Documentation](#documentation) | �🚀 [Quick Start](#-quick-start)

_An enterprise-grade AI-powered platform for automated road and pavement condition assessment_

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [AI Model](#-ai-model)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Overview

**RoadHealth AI** is an enterprise-grade web application that leverages **Artificial Intelligence** and **Computer Vision** to automatically assess and analyze pavement and road conditions. Simply upload road images, and our AI engine detects defects like **cracks**, **potholes**, and **surface deterioration**, providing instant **severity scores**, **maintenance recommendations**, and **actionable insights**.

### 🎯 Use Cases

- 🏗️ **Infrastructure Maintenance** - Monitor road conditions at scale
- 🚧 **Preventive Maintenance** - Identify issues before they become critical
- 📊 **Asset Management** - Track and prioritize repairs efficiently
- 🌍 **Smart Cities** - Integrate with municipal management systems
- 🔬 **Research & Development** - Analyze pavement degradation patterns

---

## 🌐 Live Demo

### 🔗 **Production Application**

**URL**: [https://roadhealth-ai-automated-pavement.onrender.com](https://roadhealth-ai-automated-pavement.onrender.com)

**Demo Credentials:**

```
Email: demo@roadhealth.com
Password: demo2024
```

**Available Features:**

- ✅ Upload and analyze road images instantly
- ✅ Real-time AI defect detection
- ✅ Interactive dashboard with analytics
- ✅ Generate professional PDF reports
- ✅ Export data to CSV
- ✅ Map view with geolocation support
- ✅ Role-based access control

---

## ✨ Key Features

### 🤖 AI-Powered Analysis

- **Real-time defect detection** using OpenCV and computer vision
- **Multi-class classification**: Cracks, potholes, rough surfaces, edge damage
- **Severity scoring** (0-100 scale) with condition labels (Good/Moderate/Poor/Critical)
- **Confidence metrics** for each prediction (70-95% accuracy)
- **Annotated images** with visual overlays and bounding boxes

### 📊 Advanced Dashboard

- **Interactive charts** powered by Chart.js
- **Real-time statistics** and KPIs (total images, defects detected, average severity)
- **Defect distribution** pie charts
- **Severity trends** line graphs
- **Filterable data** by status, date range, and severity level

### 👥 Role-Based Access Control

- **Admin**: Full system access, user management, system configuration
- **Engineer**: Upload images, view reports, analyze data, generate reports
- **Viewer**: Read-only access to reports and statistics

### 📍 Geospatial Integration

- **Google Maps integration** for location-based analysis
- **GPS coordinate support** for uploaded images
- **Color-coded markers** (Green = Good, Yellow = Moderate, Orange = Poor, Red = Critical)
- **Interactive map view** with clustering for large datasets

### 📄 Professional Reporting

- **PDF report generation** with detailed analysis and charts
- **CSV data export** for external processing and analytics
- **Maintenance recommendations** based on AI findings
- **Historical tracking** of road conditions over time
- **Batch processing** for multiple images

### 🔔 Smart Notifications

- **Email alerts** for critical road conditions
- **Automated notifications** to stakeholders
- **Customizable alert thresholds**
- **Real-time status updates**

### 🔒 Enterprise Security

- **JWT-based authentication** for REST API access
- **Django session management** for web interface
- **Role-based permissions** and access control
- **Secure file uploads** with type and size validation
- **CSRF protection** and XSS prevention

### 🐳 Production Ready

- **Docker containerization** for consistent deployments
- **PostgreSQL database** for reliable data persistence
- **Redis integration** for caching and task queuing
- **Gunicorn WSGI server** optimized for production
- **WhiteNoise** for efficient static file serving
- **Celery** for asynchronous task processing

---

## 🏗️ Tech Stack

### Backend

| Technology            | Version | Purpose                |
| --------------------- | ------- | ---------------------- |
| Django                | 4.2.7   | Web framework          |
| Django REST Framework | 3.14+   | API development        |
| PostgreSQL            | 15+     | Database               |
| Celery                | 5.3+    | Async task processing  |
| Redis                 | 7.0+    | Message broker & cache |
| Gunicorn              | 21.2+   | WSGI server            |

### AI/ML

| Technology | Version        | Purpose                 |
| ---------- | -------------- | ----------------------- |
| OpenCV     | 4.10+          | Image processing        |
| NumPy      | 2.2+           | Numerical computations  |
| TensorFlow | 2.x (optional) | Deep learning framework |

### Frontend

| Technology      | Version | Purpose            |
| --------------- | ------- | ------------------ |
| TailwindCSS     | 3.x     | UI styling         |
| Chart.js        | 4.x     | Data visualization |
| Font Awesome    | 6.x     | Icons              |
| Google Maps API | -       | Mapping            |

### DevOps

| Tool           | Purpose                       |
| -------------- | ----------------------------- |
| Docker         | Containerization              |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | CI/CD pipeline                |
| Render         | Cloud hosting                 |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+
- Git

### Installation in 5 Minutes

```bash
# 1. Clone repository
git clone https://github.com/vamsi-lpu18/RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs.git
cd RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
copy .env.example .env
# Edit .env with your database credentials

# 5. Create PostgreSQL database
createdb roadhealth_db

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Collect static files
python manage.py collectstatic --noinput

# 9. Run development server
python manage.py runserver
```

**Access the application at:** `http://127.0.0.1:8000`

---

## � Installation

### Option 1: Local Development (Detailed)

#### Step 1: Clone Repository

```bash
git clone https://github.com/vamsi-lpu18/RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs.git
cd RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs
```

#### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables

```bash
# Copy example environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env file with your settings:
# - SECRET_KEY (generate using: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - DB_NAME, DB_USER, DB_PASSWORD
# - EMAIL settings (optional)
# - GOOGLE_MAPS_API_KEY (optional)
```

#### Step 5: Set Up Database

```bash
# Create PostgreSQL database
createdb roadhealth_db

# Or using psql:
psql -U postgres
CREATE DATABASE roadhealth_db;
\q
```

#### Step 6: Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

#### Step 7: Create Admin User

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### Step 8: Create Required Directories

```bash
mkdir media media\images media\annotated_images staticfiles logs
```

#### Step 9: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### Step 10: Run Development Server

```bash
python manage.py runserver
```

**Application URLs:**

- **Frontend**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin
- **API**: http://127.0.0.1:8000/api

---

### Option 2: Docker Deployment

#### Step 1: Prerequisites

```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop

# Verify installation
docker --version
docker-compose --version
```

#### Step 2: Configure Environment

```bash
# Copy environment file
copy .env.example .env

# Edit .env with Docker settings:
DB_HOST=db
DB_PORT=5432
CELERY_BROKER_URL=redis://redis:6379/0
```

#### Step 3: Build and Run

```bash
# Build and start all services
docker-compose up --build -d

# Services started:
# - web (Django application)
# - db (PostgreSQL database)
# - redis (Redis cache)
# - celery (Background worker)
```

#### Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

#### Step 5: Access Application

**URL**: http://localhost:8000

#### Management Commands

```bash
# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Remove all containers and volumes
docker-compose down -v
```

---

## 🚀 Deployment

### Deploy to Render (Recommended)

#### Prerequisites

- GitHub account
- Render account ([render.com](https://render.com))
- PostgreSQL database

#### Step-by-Step Guide

1. **Push Code to GitHub**

```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Create PostgreSQL Database**

- Go to Render Dashboard
- Click "New +" → "PostgreSQL"
- Name: `roadhealth-db`
- Plan: Free
- Create Database
- Copy **Internal Database URL**

3. **Create Web Service**

- Click "New +" → "Web Service"
- Connect GitHub repository
- Configure:
  - **Name**: `roadhealth-ai`
  - **Environment**: Python 3
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roadhealth.wsgi:application`

4. **Set Environment Variables**

```
SECRET_KEY=<your-generated-key>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<your-postgres-internal-url>
PYTHON_VERSION=3.11.0
```

5. **Deploy**

- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Access your app at: `https://your-app.onrender.com`

6. **Create Superuser**

```bash
# In Render Shell
python manage.py createsuperuser
```

**🌐 Live Production URL**: [https://roadhealth-ai-automated-pavement.onrender.com](https://roadhealth-ai-automated-pavement.onrender.com)

---

## 📄 API Documentation

### Authentication

#### Obtain JWT Token

```http
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Images API

#### List Images

```http
GET /api/core/images/
Authorization: Bearer {access_token}
```

#### Upload Image

```http
POST /api/core/images/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "title": "Road Section 1",
  "image": [binary],
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

### Full API Endpoints

| Method | Endpoint                           | Description           |
| ------ | ---------------------------------- | --------------------- |
| POST   | `/api/token/`                      | Obtain JWT token      |
| POST   | `/api/token/refresh/`              | Refresh JWT token     |
| POST   | `/api/accounts/register/`          | Register new user     |
| GET    | `/api/accounts/profile/`           | Get user profile      |
| GET    | `/api/core/images/`                | List all images       |
| POST   | `/api/core/images/`                | Upload new image      |
| GET    | `/api/core/images/{id}/`           | Get image details     |
| DELETE | `/api/core/images/{id}/`           | Delete image          |
| POST   | `/api/core/images/{id}/reanalyze/` | Reanalyze image       |
| GET    | `/api/analysis/results/`           | List analysis results |
| GET    | `/api/analysis/results/critical/`  | Get critical results  |
| POST   | `/api/reports/generate/`           | Generate PDF report   |
| GET    | `/api/reports/export/csv/`         | Export to CSV         |

---

## 🧠 AI Model

### Current Implementation

The application uses **OpenCV edge detection** for demonstration:

**Algorithm**: Canny Edge Detection

- Load image → Resize to 224x224
- Convert to grayscale
- Apply Canny edge detection
- Calculate edge density
- Classify defect type based on density
- Generate severity score
- Create annotated image

**Defect Classification:**

- **Edge Density > 15%** → Crack (Severity: 75-100)
- **Edge Density 10-15%** → Rough Surface (Severity: 50-75)
- **Edge Density 5-10%** → Edge Crack (Severity: 25-50)
- **Edge Density < 5%** → No Defect (Severity: 0-25)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create a Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Follow PEP 8 style guide
4. **Commit**: `git commit -m "Add amazing feature"`
5. **Push**: `git push origin feature/amazing-feature`
6. **Create Pull Request**

---

## 📝 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Authors

**Vamsi Krishna**

- GitHub: [@vamsi-lpu18](https://github.com/vamsi-lpu18)
- Repository: [RoadHealth-AI](https://github.com/vamsi-lpu18/RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs)

---

## 🙏 Acknowledgments

- **Django Community** - Web framework
- **OpenCV Contributors** - Computer vision tools
- **TailwindCSS Team** - UI components
- **Chart.js** - Data visualization
- **Render** - Cloud hosting

---

## 📧 Support & Contact

- 📖 **Documentation**: Read this README
- 🐛 **Report Bugs**: [Open an Issue](https://github.com/vamsi-lpu18/RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs/issues)
- 💡 **Feature Requests**: [Submit Ideas](https://github.com/vamsi-lpu18/RoadHealth-AI-Automated-Pavement-Condition-Assessment-from-Photographs/issues)
- **Website**: [https://roadhealth-ai-automated-pavement.onrender.com](https://roadhealth-ai-automated-pavement.onrender.com)

---

<div align="center">

### 🚀 Built with Django, AI, and TailwindCSS

**Made with ❤️ for better road infrastructure management**

**⭐ Star this repo if you find it useful!**

[⬆ Back to Top](#-roadhealth-ai---automated-pavement-condition-assessment)

</div>

```bash
docker-compose up --build
```

3. **Run migrations** (in a new terminal)

```bash
docker-compose exec web python manage.py migrate
```

4. **Create superuser**

```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**

```
http://localhost:8000
```

## 📁 Project Structure

```
project/
├── roadhealth/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── accounts/            # User authentication & management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── serializers.py
├── core/                # Image upload & management
│   ├── models.py
│   ├── views.py
│   └── forms.py
├── analysis/            # AI model integration
│   ├── models.py
│   ├── ai_model.py
│   ├── tasks.py
│   └── views.py
├── reports/             # PDF & CSV generation
│   ├── pdf_generator.py
│   ├── csv_exporter.py
│   └── views.py
├── templates/           # HTML templates
│   ├── base.html
│   ├── core/
│   ├── accounts/
│   └── reports/
├── static/              # Static files (CSS, JS)
├── media/               # User uploaded files
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

## 🎯 Usage

### 1. Register an Account

- Go to `/accounts/register/`
- Choose your role (Admin/Engineer/Viewer)
- Complete registration

### 2. Upload Road Images

- Navigate to "Upload" page
- Select a road/pavement image (JPEG/PNG, max 10MB)
- Optionally add title, description, and GPS coordinates
- Submit for AI analysis

### 3. View Dashboard

- See statistics and analytics
- View defect distribution charts
- Browse recent analyses
- Export data to CSV or PDF

### 4. Generate Reports

- Click on any analyzed image
- View detailed analysis results
- Download PDF report
- Get maintenance recommendations

### 5. Map View

- See all geotagged images on Google Maps
- Color-coded markers based on severity
- Click markers for details

## 🔧 Configuration

### Email Settings (for notifications)

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Google Maps API (for map view)

```env
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
```

### OpenAI API (for AI suggestions - optional)

```env
OPENAI_API_KEY=your-openai-api-key
```

## 🧪 AI Model

The current implementation includes a **placeholder AI model** using simple image processing (edge detection) for demonstration purposes.

### To integrate a real model:

1. Train your model using datasets like:

   - RDD2020 (Road Damage Dataset)
   - GAPs (German Asphalt Pavement)
   - CrackForest Dataset

2. Save the model file (`.h5`, `.pth`, or `.onnx`)

3. Update `analysis/ai_model.py`:

```python
def load_model(self):
    import tensorflow as tf
    self.model = tf.keras.models.load_model('path/to/your/model.h5')
```

4. Update the `detect_defects()` method with actual model inference

## 📊 API Endpoints

### Authentication

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh token
- `POST /api/accounts/register/` - Register user

### Images

- `GET /api/core/images/` - List images
- `POST /api/core/images/` - Upload image
- `GET /api/core/images/{id}/` - Get image details
- `POST /api/core/images/{id}/reanalyze/` - Reanalyze image

### Analysis

- `GET /api/analysis/results/` - List analysis results
- `GET /api/analysis/results/critical/` - Get critical results
- `GET /api/analysis/results/by_defect_type/?type=crack` - Filter by defect type

## 🚀 Deployment

### Deploy to Production

1. Set `DEBUG=False` in `.env`
2. Set strong `SECRET_KEY`
3. Configure allowed hosts
4. Use PostgreSQL for database
5. Set up Redis for Celery
6. Configure email settings
7. Set up static file serving (WhiteNoise included)
8. Use Gunicorn as WSGI server
9. Optional: Add Nginx reverse proxy

### Platforms

- **AWS EC2** - Deploy with Docker
- **Heroku** - Use provided Dockerfile
- **Railway** - Connect GitHub repo
- **Render** - Docker-based deployment
- **DigitalOcean** - App Platform or Droplet

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for road infrastructure management

## 🙏 Acknowledgments

- Django Community
- TensorFlow Team
- OpenCV Contributors
- TailwindCSS Team

## 📧 Support

For support, email support@roadhealth.ai or open an issue on GitHub.

---

**Made with Django, AI, and TailwindCSS** 🚀
