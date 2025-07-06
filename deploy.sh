#!/bin/bash

# Blood Bank Management System - Deployment Script
# This script helps you deploy your Django app to various platforms

echo "🚀 Blood Bank Management System - Deployment Helper"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if all required files exist
echo "📋 Checking deployment files..."

required_files=("railway.json" "requirements_production.txt" "build.sh" "nixpacks.toml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ Missing required deployment files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo "Please ensure all deployment files are present."
    exit 1
fi

echo "✅ All deployment files found!"

# Generate secret key if not exists
if [ -z "$SECRET_KEY" ]; then
    echo "🔑 Generating new SECRET_KEY..."
    export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
    echo "SECRET_KEY generated: $SECRET_KEY"
fi

# Check current branch
current_branch=$(git branch --show-current)
echo "🌿 Current branch: $current_branch"

# Show deployment options
echo ""
echo "🎯 Choose your deployment platform:"
echo "1. Railway (Recommended - Free & Easy)"
echo "2. Heroku"
echo "3. DigitalOcean App Platform"
echo "4. Traditional VPS"
echo "5. Test locally with production settings"
echo "6. Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "Steps to deploy to Railway:"
        echo "1. Go to https://railway.app"
        echo "2. Sign up/Login with GitHub"
        echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "4. Select your blood bank repository"
        echo "5. Add these environment variables in Railway dashboard:"
        echo "   DEBUG=False"
        echo "   SECRET_KEY=$SECRET_KEY"
        echo "   ALLOWED_HOSTS=your-app-name.railway.app"
        echo "6. Railway will automatically deploy your app"
        echo ""
        echo "After deployment, run these commands in Railway:"
        echo "   python manage.py migrate"
        echo "   python manage.py createsuperuser"
        ;;
    2)
        echo "🌊 Deploying to Heroku..."
        echo ""
        echo "Prerequisites:"
        echo "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Login to Heroku: heroku login"
        echo ""
        echo "Deployment commands:"
        echo "heroku create your-bloodbank-app"
        echo "heroku addons:create heroku-postgresql:mini"
        echo "heroku config:set SECRET_KEY='$SECRET_KEY'"
        echo "heroku config:set DEBUG=False"
        echo "git push heroku $current_branch:main"
        echo "heroku run python manage.py migrate"
        echo "heroku run python manage.py createsuperuser"
        ;;
    3)
        echo "🌊 Deploying to DigitalOcean App Platform..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://cloud.digitalocean.com/apps"
        echo "2. Create new app from GitHub repository"
        echo "3. Select your blood bank repository"
        echo "4. Configure build settings:"
        echo "   - Build Command: ./build.sh"
        echo "   - Run Command: gunicorn bloodbankmanagement.wsgi:application --bind 0.0.0.0:\$PORT"
        echo "5. Add environment variables:"
        echo "   DEBUG=False"
        echo "   SECRET_KEY=$SECRET_KEY"
        echo "   ALLOWED_HOSTS=your-app-name.ondigitalocean.app"
        ;;
    4)
        echo "🖥️ Traditional VPS Deployment..."
        echo ""
        echo "This requires manual server setup. See DEPLOYMENT_GUIDE.md for detailed instructions."
        echo ""
        echo "Quick commands for VPS:"
        echo "sudo apt update && sudo apt upgrade -y"
        echo "sudo apt install python3 python3-pip nginx postgresql postgresql-contrib -y"
        echo "git clone https://github.com/your-username/bloodbankmanagement.git"
        echo "cd bloodbankmanagement"
        echo "python3 -m venv venv"
        echo "source venv/bin/activate"
        echo "pip install -r requirements_production.txt"
        ;;
    5)
        echo "🧪 Testing locally with production settings..."
        echo ""
        echo "Setting environment variables for local testing..."
        export DEBUG=False
        export SECRET_KEY="$SECRET_KEY"
        export ALLOWED_HOSTS="localhost,127.0.0.1"
        
        echo "Running with production settings..."
        python manage.py collectstatic --noinput
        python manage.py runserver 8000
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
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo "🔧 For troubleshooting, check the logs and environment variables"
echo ""
echo "🎉 Happy deploying!" 