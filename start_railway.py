#!/usr/bin/env python
"""
Railway startup script for Blood Bank Management System
"""
import os
import sys

def main():
    print("🚀 Starting Blood Bank Management System on Railway...")
    
    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodbankmanagement.settings_railway')
    
    # Get port from Railway
    port = os.environ.get('PORT', '8000')
    
    print(f"📋 Environment:")
    print(f"   - DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"   - PORT: {port}")
    print(f"   - SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
    
    # Import Django and run management commands
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Set up Django
        django.setup()
        
        # Run migrations
        print("🗄️ Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        # Start Gunicorn
        print(f"🌐 Starting Gunicorn on port {port}...")
        os.system(f"gunicorn bloodbankmanagement.wsgi:application --bind 0.0.0.0:{port} --timeout 120 --workers 1")
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 