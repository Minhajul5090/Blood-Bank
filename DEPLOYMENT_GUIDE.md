# 🚀 Blood Bank Management System - Deployment Guide

This guide covers multiple deployment options for the Django Blood Bank Management System.

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Option 1: Heroku Deployment](#option-1-heroku-deployment)
3. [Option 2: Railway Deployment](#option-2-railway-deployment)
4. [Option 3: DigitalOcean App Platform](#option-3-digitalocean-app-platform)
5. [Option 4: Traditional VPS Deployment](#option-4-traditional-vps-deployment)
6. [Production Settings Configuration](#production-settings-configuration)
7. [Database Migration](#database-migration)
8. [Static Files Configuration](#static-files-configuration)
9. [Security Considerations](#security-considerations)
10. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Updated `DEBUG = False` in settings
- [ ] Generated a new `SECRET_KEY`
- [ ] Configured `ALLOWED_HOSTS`
- [ ] Set up environment variables
- [ ] Updated database configuration
- [ ] Configured static files
- [ ] Set up email settings
- [ ] Created production requirements.txt

---

## 🎯 Option 1: Heroku Deployment

### Step 1: Prepare for Heroku

Create the following files in your project root:

**`Procfile`** (no file extension):

```
web: gunicorn bloodbankmanagement.wsgi --log-file -
```

**`runtime.txt`**:

```
python-3.9.18
```

**Update `requirements.txt`**:

```
# Core Django Framework
Django==3.0.5

# Database and ORM
sqlparse==0.3.1

# Web Server Gateway Interface
asgiref==3.0.5

# Time Zone Support
pytz==2020.1

# Form Enhancement
django-widget-tweaks==1.4.8

# Image Processing (for profile pictures)
Pillow==8.0.1

# Production Server
gunicorn==20.0.4

# Static Files
whitenoise==5.2.0

# Database (for Heroku)
dj-database-url==0.5.0
psycopg2-binary==2.8.6
```

### Step 2: Update Settings for Heroku

Create `bloodbankmanagement/settings_production.py`:

```python
import os
import dj_database_url
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

ALLOWED_HOSTS = [
    'your-app-name.herokuapp.com',
    'localhost',
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Step 3: Deploy to Heroku

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-bloodbank-app

# Add PostgreSQL database
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set EMAIL_HOST_USER="your-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="your-app-password"

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Open the app
heroku open
```

---

## 🚂 Option 2: Railway Deployment

### Step 1: Prepare for Railway

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn bloodbankmanagement.wsgi --log-file -",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables in Railway dashboard
4. Deploy automatically

---

## 🌊 Option 3: DigitalOcean App Platform

### Step 1: Prepare for DigitalOcean

Create `.do/app.yaml`:

```yaml
name: bloodbank-management
services:
  - name: web
    source_dir: /
    github:
      repo: your-username/your-repo
      branch: main
    run_command: gunicorn bloodbankmanagement.wsgi --log-file -
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
      - key: SECRET_KEY
        value: ${SECRET_KEY}
      - key: DATABASE_URL
        value: ${DATABASE_URL}
      - key: EMAIL_HOST_USER
        value: ${EMAIL_HOST_USER}
      - key: EMAIL_HOST_PASSWORD
        value: ${EMAIL_HOST_PASSWORD}
```

### Step 2: Deploy to DigitalOcean

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Connect your GitHub repository
3. Configure environment variables
4. Deploy

---

## 🖥️ Option 4: Traditional VPS Deployment

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Create project directory
sudo mkdir /var/www/bloodbank
sudo chown $USER:$USER /var/www/bloodbank
```

### Step 2: Application Setup

```bash
# Clone your repository
cd /var/www/bloodbank
git clone https://github.com/your-username/your-repo.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:password@localhost/bloodbank"
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"
```

### Step 3: Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE bloodbank;
CREATE USER bloodbank_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bloodbank TO bloodbank_user;
\q

# Run migrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 4: Gunicorn Configuration

Create `/etc/systemd/system/bloodbank.service`:

```ini
[Unit]
Description=Blood Bank Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bloodbank
Environment="PATH=/var/www/bloodbank/venv/bin"
ExecStart=/var/www/bloodbank/venv/bin/gunicorn --workers 3 --bind unix:/var/www/bloodbank/bloodbank.sock bloodbankmanagement.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 5: Nginx Configuration

Create `/etc/nginx/sites-available/bloodbank`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/bloodbank;
    }

    location /media/ {
        root /var/www/bloodbank;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/bloodbank/bloodbank.sock;
    }
}
```

### Step 6: Final Setup

```bash
# Collect static files
python manage.py collectstatic

# Start services
sudo systemctl start bloodbank
sudo systemctl enable bloodbank
sudo ln -s /etc/nginx/sites-available/bloodbank /etc/nginx/sites-enabled
sudo systemctl restart nginx

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## ⚙️ Production Settings Configuration

### Update `bloodbankmanagement/settings.py`:

```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # Add this for static files
    'widget_tweaks',
    'blood',
    'donor',
    'patient',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'bloodbank'),
        'USER': os.environ.get('DB_USER', 'bloodbank_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

## 🗄️ Database Migration

### For PostgreSQL:

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update settings.py DATABASES configuration
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 📁 Static Files Configuration

```bash
# Collect static files
python manage.py collectstatic --noinput

# Configure whitenoise for static files
# Add to MIDDLEWARE after SecurityMiddleware
'whitenoise.middleware.WhiteNoiseMiddleware',

# Add to settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 🔒 Security Considerations

### 1. Environment Variables

```bash
# Never commit sensitive data
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@host/db"
export EMAIL_HOST_PASSWORD="your-app-password"
```

### 2. Update requirements.txt

```
# Add security packages
django-cors-headers==3.10.0
django-ratelimit==2.0.0
```

### 3. Security Headers

```python
# Add to settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

---

## 📊 Monitoring and Maintenance

### 1. Logging Configuration

```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Health Check Endpoint

Create `blood/views.py`:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

### 3. Backup Strategy

```bash
# Database backup
pg_dump bloodbank > backup_$(date +%Y%m%d_%H%M%S).sql

# Media files backup
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

---

## 🚀 Quick Deployment Commands

### For Heroku:

```bash
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### For Railway:

```bash
# Just push to GitHub and connect to Railway
git push origin main
```

### For DigitalOcean:

```bash
# Connect GitHub repo to DigitalOcean App Platform
# Configure environment variables in dashboard
```

---

## 📞 Support

If you encounter issues during deployment:

1. Check the logs: `heroku logs --tail` (Heroku)
2. Verify environment variables are set correctly
3. Ensure all dependencies are in requirements.txt
4. Test locally with production settings

---

## 🔄 Post-Deployment Checklist

- [ ] SSL certificate is working
- [ ] Static files are loading correctly
- [ ] Database migrations are complete
- [ ] Email functionality is working
- [ ] Admin interface is accessible
- [ ] File uploads are working
- [ ] All forms are functional
- [ ] Mobile responsiveness is maintained
- [ ] Performance is acceptable
- [ ] Monitoring is set up

---

**🎉 Congratulations! Your Blood Bank Management System is now deployed and ready to save lives!**
