"""
WSGI config for alfa_recovery project on PythonAnywhere.

This file contains the WSGI configuration required by PythonAnywhere.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/alfarecovery/ALFA/'  # Path to the directory containing manage.py
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfa_recovery.settings'

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
