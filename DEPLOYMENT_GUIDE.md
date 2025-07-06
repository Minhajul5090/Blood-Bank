# 🚀 Blood Bank Management System - Deployment Guide

## Quick Start: Railway Deployment (Recommended)

### Step 1: Prepare Your Repository

1. Make sure all files are committed to Git
2. Ensure you have the following files in your project root:
   - `railway.json`
   - `requirements_production.txt`
   - `build.sh`
   - `nixpacks.toml`

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your blood bank repository
5. Railway will automatically detect the configuration and deploy

### Step 3: Configure Environment Variables

In Railway dashboard, add these environment variables:

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-app-name.railway.app
DATABASE_URL=your-database-url
```

### Step 4: Run Database Migrations

In Railway dashboard:

1. Go to your project
2. Click on "Variables" tab
3. Add command: `python manage.py migrate`
4. Add command: `python manage.py createsuperuser`

## Option 2: Heroku Deployment

### Step 1: Install Heroku CLI

```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
heroku login
heroku create your-bloodbank-app
```

### Step 3: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Step 5: Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Option 3: DigitalOcean App Platform

### Step 1: Create App

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub repository
3. Select your blood bank repository

### Step 2: Configure Build Settings

- Build Command: `./build.sh`
- Run Command: `gunicorn bloodbankmanagement.wsgi:application --bind 0.0.0.0:$PORT`

### Step 3: Add Environment Variables

```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-app-name.ondigitalocean.app
```

## Option 4: Traditional VPS Deployment

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Nginx, PostgreSQL
sudo apt install python3 python3-pip nginx postgresql postgresql-contrib -y
```

### Step 2: Clone Repository

```bash
git clone https://github.com/your-username/bloodbankmanagement.git
cd bloodbankmanagement
```

### Step 3: Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_production.txt
```

### Step 4: Configure Database

```bash
sudo -u postgres psql
CREATE DATABASE bloodbank;
CREATE USER bloodbankuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE bloodbank TO bloodbankuser;
\q
```

### Step 5: Configure Django Settings

Update `settings_production.py` with your database credentials.

### Step 6: Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Step 7: Setup Gunicorn

```bash
sudo apt install gunicorn -y
```

Create systemd service file:

```bash
sudo nano /etc/systemd/system/bloodbank.service
```

Add content:

```ini
[Unit]
Description=Blood Bank Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind unix:/path/to/project/bloodbank.sock bloodbankmanagement.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Step 8: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/bloodbank
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/project/bloodbank.sock;
    }
}
```

### Step 9: Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/bloodbank /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl start bloodbank
sudo systemctl enable bloodbank
```

## Environment Variables Reference

### Required Variables

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

### Optional Variables

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS in production
- [ ] Set up proper database credentials
- [ ] Configure static files serving
- [ ] Set up proper logging
- [ ] Configure email settings

## Troubleshooting

### Common Issues:

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database connection errors**: Check database credentials
3. **500 errors**: Check logs and ensure all environment variables are set
4. **Migration errors**: Run `python manage.py migrate --run-syncdb`

### Logs Location:

- Railway: Dashboard → Deployments → View logs
- Heroku: `heroku logs --tail`
- DigitalOcean: App Platform → Logs tab
- VPS: `/var/log/nginx/error.log` and systemd logs

## Post-Deployment Steps

1. **Create Superuser**: Set up admin account
2. **Configure Email**: For password reset functionality
3. **Set up Monitoring**: Monitor app performance
4. **Configure Backups**: Regular database backups
5. **SSL Certificate**: Enable HTTPS
6. **Domain Setup**: Point your domain to the app

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure database migrations are complete
4. Test locally with production settings

---

**Recommended for beginners**: Railway deployment
**Best for scalability**: DigitalOcean App Platform
**Most control**: Traditional VPS deployment
