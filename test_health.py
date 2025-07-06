#!/usr/bin/env python
"""
Test script to verify health check works
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodbankmanagement.settings_railway')
django.setup()

# Test the health check
from blood.views import health_check
from django.test import RequestFactory

def test_health_check():
    print("🧪 Testing health check endpoint...")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/health/')
    
    # Call the health check
    response = health_check(request)
    
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response['Content-Type']}")
    print(f"Response: {response.content.decode()}")
    
    if response.status_code == 200:
        print("✅ Health check working correctly!")
        return True
    else:
        print("❌ Health check failed!")
        return False

if __name__ == '__main__':
    test_health_check() 