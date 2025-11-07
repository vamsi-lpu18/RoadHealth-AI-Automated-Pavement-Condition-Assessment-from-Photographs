# RoadHealth AI - Automated Pavement Condition Assessment

![RoadHealth AI](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Deployment](https://img.shields.io/badge/Deployed-Render-success)

## 🚀 Overview

**RoadHealth AI** is a comprehensive web application that uses artificial intelligence to automatically assess pavement and road conditions. Upload images of roads or pavements, and the AI model will detect defects like cracks, potholes, and surface issues, providing severity scores and maintenance recommendations.

## ✨ Features

- 🤖 **AI-Powered Analysis**: Detect cracks, potholes, and surface defects using computer vision
- 📊 **Real-Time Dashboard**: Interactive charts and statistics with Chart.js
- 👥 **Role-Based Access**: Admin, Engineer, and Viewer roles with different permissions
- 📍 **Geolocation Support**: Map view with Google Maps integration
- 📄 **Professional Reports**: Generate PDF reports and export data to CSV
- 📧 **Email Notifications**: Automatic alerts for critical road conditions
- 🐳 **Docker Ready**: Fully containerized with Docker and Docker Compose
- 🔒 **Secure Authentication**: JWT-based API authentication
- 📱 **Responsive UI**: Modern interface built with TailwindCSS

## 🏗️ Tech Stack

### Backend

- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Celery** - Asynchronous task processing
- **Redis** - Message broker and cache

### AI/ML

- **OpenCV** - Image processing
- **TensorFlow** - Deep learning (model placeholder included)
- **NumPy** - Numerical computations

### Frontend

- **TailwindCSS** - Utility-first CSS framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons

### DevOps

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Gunicorn** - WSGI server
- **Nginx** (optional) - Reverse proxy

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (for containerized deployment)

## 🛠️ Installation

### Option 1: Local Development

1. **Clone the repository**

```bash
git clone <repository-url>
cd project
```

2. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
copy .env.example .env
# Edit .env with your configuration
```

5. **Set up PostgreSQL database**

```bash
# Create database named 'roadhealth_db'
createdb roadhealth_db
```

6. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**

```bash
python manage.py createsuperuser
```

8. **Create static directories**

```bash
mkdir static
mkdir media
mkdir logs
```

9. **Run development server**

```bash
python manage.py runserver
```

10. **Start Celery worker** (in a new terminal)

```bash
celery -A roadhealth worker --loglevel=info
```

### Option 2: Docker Deployment

1. **Copy environment file**

```bash
copy .env.example .env
# Edit .env with your configuration
```

2. **Build and run containers**

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
