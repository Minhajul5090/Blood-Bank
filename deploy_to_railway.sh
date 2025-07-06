#!/bin/bash

echo "🚀 Deploying Blood Bank Management System to Railway..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Add all changes
echo "📦 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Fix Railway health check and deployment configuration"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo "✅ Deployment script completed!"
echo "🌐 Railway will automatically deploy from your GitHub repository"
echo "⏳ Please wait a few minutes for the deployment to complete"
echo "🔍 Check your Railway dashboard for deployment status" 