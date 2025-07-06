#!/bin/bash

# Blood Bank Management System - Build Script for Railway
echo "🚀 Building Blood Bank Management System..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_production.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!" 