#!/bin/bash

# Railway Deployment Fix Script
echo "🚂 Fixing Railway Deployment Issues..."

# Step 1: Activate virtual environment
echo "📦 Activating virtual environment..."
source env/Scripts/activate

# Step 2: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_railway.txt

# Step 3: Test locally
echo "🧪 Testing locally..."
python manage.py check --deploy
python manage.py collectstatic --noinput

# Step 4: Generate new secret key
echo "🔑 Generating new SECRET_KEY..."
python generate_secret.py

# Step 5: Commit and push
echo "📝 Committing changes..."
git add .
git commit -m "Fix Railway build configuration"
git push origin main

echo "✅ Railway deployment fix completed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Railway dashboard"
echo "2. Check the latest deployment"
echo "3. Monitor build logs"
echo "4. Set environment variables if needed" 