#!/bin/bash

# Railway Deployment Script for Blood Bank Management System

echo "🚀 Starting Railway deployment..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Set environment variables for Railway
export DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway
export PYTHONPATH=$PWD

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔧 Setting up initial data..."
python manage.py shell -c "
from blood.models import Stock
from django.contrib.auth.models import Group

# Create blood groups if they don't exist
blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
for bg in blood_groups:
    Stock.objects.get_or_create(bloodgroup=bg, defaults={'unit': 0})

# Create user groups if they don't exist
groups = ['DONOR', 'PATIENT']
for group_name in groups:
    Group.objects.get_or_create(name=group_name)

print('✅ Initial data setup complete')
"

echo "✅ Railway deployment setup complete!"
echo "🌐 Your app should now be accessible at your Railway URL"
echo "🔍 Health check endpoint: /health/" 