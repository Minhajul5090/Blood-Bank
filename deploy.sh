#!/bin/bash

# Blood Bank Management System - Deployment Script
# This script helps automate the deployment process

echo "🚀 Blood Bank Management System - Deployment Script"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Function to generate secret key
generate_secret_key() {
    python3 -c "import secrets; print(secrets.token_urlsafe(50))"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "📋 Pre-deployment checklist:"
echo "1. Checking Python version..."
python3 --version

echo "2. Checking if virtual environment is activated..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment is active: $VIRTUAL_ENV"
else
    echo "⚠️  Virtual environment not detected. Consider activating one."
fi

echo "3. Installing/updating dependencies..."
pip install -r requirements_production.txt

echo "4. Running Django system checks..."
python manage.py check --deploy

echo "5. Collecting static files..."
python manage.py collectstatic --noinput

echo "6. Running database migrations..."
python manage.py migrate

echo "7. Checking for environment variables..."
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  SECRET_KEY not set. Generating one..."
    export SECRET_KEY=$(generate_secret_key)
    echo "Generated SECRET_KEY: $SECRET_KEY"
fi

if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL not set. Using SQLite for development."
fi

if [ -z "$EMAIL_HOST_USER" ]; then
    echo "⚠️  EMAIL_HOST_USER not set. Email functionality may not work."
fi

if [ -z "$EMAIL_HOST_PASSWORD" ]; then
    echo "⚠️  EMAIL_HOST_PASSWORD not set. Email functionality may not work."
fi

echo ""
echo "🎯 Choose your deployment platform:"
echo "1. Heroku"
echo "2. Railway"
echo "3. DigitalOcean App Platform"
echo "4. Traditional VPS"
echo "5. Local Production Test"
echo "6. Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "🚀 Deploying to Heroku..."
        if ! command_exists heroku; then
            echo "❌ Heroku CLI not found. Please install it first:"
            echo "   https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo "📝 Heroku deployment steps:"
        echo "1. Login to Heroku: heroku login"
        echo "2. Create app: heroku create your-app-name"
        echo "3. Add database: heroku addons:create heroku-postgresql:hobby-dev"
        echo "4. Set environment variables:"
        echo "   heroku config:set SECRET_KEY=\"$SECRET_KEY\""
        echo "   heroku config:set EMAIL_HOST_USER=\"your-email@gmail.com\""
        echo "   heroku config:set EMAIL_HOST_PASSWORD=\"your-app-password\""
        echo "5. Deploy: git push heroku main"
        echo "6. Run migrations: heroku run python manage.py migrate"
        echo "7. Create superuser: heroku run python manage.py createsuperuser"
        ;;
    2)
        echo "🚂 Deploying to Railway..."
        echo "📝 Railway deployment steps:"
        echo "1. Go to https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Add environment variables in Railway dashboard:"
        echo "   - SECRET_KEY: $SECRET_KEY"
        echo "   - DATABASE_URL: (will be auto-provided)"
        echo "   - EMAIL_HOST_USER: your-email@gmail.com"
        echo "   - EMAIL_HOST_PASSWORD: your-app-password"
        echo "4. Deploy automatically"
        ;;
    3)
        echo "🌊 Deploying to DigitalOcean App Platform..."
        echo "📝 DigitalOcean deployment steps:"
        echo "1. Go to https://cloud.digitalocean.com/apps"
        echo "2. Connect your GitHub repository"
        echo "3. Configure environment variables:"
        echo "   - SECRET_KEY: $SECRET_KEY"
        echo "   - DATABASE_URL: (will be auto-provided)"
        echo "   - EMAIL_HOST_USER: your-email@gmail.com"
        echo "   - EMAIL_HOST_PASSWORD: your-app-password"
        echo "4. Deploy"
        ;;
    4)
        echo "🖥️  Traditional VPS Deployment..."
        echo "📝 VPS deployment steps:"
        echo "1. Set up server with Ubuntu/Debian"
        echo "2. Install dependencies:"
        echo "   sudo apt update && sudo apt upgrade -y"
        echo "   sudo apt install python3 python3-pip python3-venv nginx postgresql -y"
        echo "3. Clone repository and set up virtual environment"
        echo "4. Configure PostgreSQL database"
        echo "5. Set up Gunicorn and Nginx"
        echo "6. Configure firewall and SSL"
        echo ""
        echo "📖 See DEPLOYMENT_GUIDE.md for detailed VPS instructions"
        ;;
    5)
        echo "🧪 Local Production Test..."
        echo "Testing with production settings..."
        
        # Set production environment variables
        export DEBUG=False
        export DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_production
        
        echo "Running production server..."
        echo "Press Ctrl+C to stop"
        gunicorn bloodbankmanagement.wsgi --bind 0.0.0.0:8000
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please select 1-6."
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment script completed!"
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "🔧 For troubleshooting, check the logs and environment variables" 