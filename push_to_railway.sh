#!/bin/bash

echo "🚂 Pushing to GitHub for Railway deployment..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check git status
echo "📋 Checking git status..."
git status

# Add all files
echo "📦 Adding all files..."
git add .

# Commit changes
echo "📝 Committing changes..."
git commit -m "Fix Railway build - use minimal requirements"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Railway dashboard"
echo "2. Check the latest deployment"
echo "3. Monitor build logs"
echo "4. If build fails, check the logs for specific errors" 