"""
WSGI config for bloodbankmanagement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use Railway settings if DJANGO_SETTINGS_MODULE is not set
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodbankmanagement.settings_railway')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodbankmanagement.settings')

application = get_wsgi_application()
