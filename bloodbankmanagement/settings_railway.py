"""
Railway-specific settings for Blood Bank Management System
"""
import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Railway provides the PORT environment variable
ALLOWED_HOSTS = ['*']

# Get SECRET_KEY from environment or use default
SECRET_KEY = os.environ.get('SECRET_KEY', 'w@k#6^!z8$1b2r4e7u0p9s3c5t!g&h@j*lqzv')

# Database configuration for Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,  # Add timeout for SQLite
        }
    }
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Media files configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email configuration (you can set these as environment variables)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Disable whitenoise for Railway (can cause issues)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' 