#!/usr/bin/env python
"""
Railway startup script for Blood Bank Management System
"""
import os
import sys
import subprocess

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
    
    try:
        # Run migrations
        print("🗄️ Running database migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        # Collect static files
        print("📁 Collecting static files...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        
        # Start Gunicorn
        print(f"🌐 Starting Gunicorn on port {port}...")
        subprocess.run([
            sys.executable, '-m', 'gunicorn',
            'bloodbankmanagement.wsgi:application',
            '--bind', f'0.0.0.0:{port}',
            '--timeout', '120',
            '--workers', '1',
            '--access-logfile', '-',
            '--error-logfile', '-'
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during startup: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 