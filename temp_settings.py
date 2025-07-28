from alfa_recovery.settings import *
DEBUG = True
ALLOWED_HOSTS = ['*']
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
