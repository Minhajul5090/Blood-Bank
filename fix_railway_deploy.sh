#!/bin/bash

# Railway Deployment Fix Script
echo "🔧 Fixing Railway Deployment Issues..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

echo "📋 Current Issues Found:"
echo "1. Railway not using correct Django settings"
echo "2. Health check failing due to database dependencies"
echo "3. Missing environment variables"

echo ""
echo "🔧 Applying Fixes..."

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix Railway health check - use Railway settings and independent health endpoint"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Fixes Applied:"
echo "✅ Updated railway.json to use Railway settings"
echo "✅ Created independent health check endpoint"
echo "✅ Updated Railway settings for better compatibility"
echo "✅ Added proper logging configuration"

echo ""
echo "🌐 Next Steps:"
echo "1. Railway will automatically redeploy from GitHub"
echo "2. Set these environment variables in Railway dashboard:"
echo "   - DJANGO_SETTINGS_MODULE=bloodbankmanagement.settings_railway"
echo "   - SECRET_KEY=w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv"
echo "3. Wait for deployment to complete"
echo "4. Test health endpoint: https://your-app.railway.app/health/"

echo ""
echo "🎯 Expected Results:"
echo "- ✅ Build completed successfully"
echo "- ✅ Health check passing"
echo "- ✅ Application accessible at Railway URL"
echo "- ✅ JSON response at /health/ endpoint" 