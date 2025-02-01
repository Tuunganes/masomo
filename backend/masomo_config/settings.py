import os
from pathlib import Path

# Define BASE_DIR for the root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Installed apps (add your app here)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',  # Your student management app
]

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend/templates'],  # Path to your templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Needed for sessions
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Needed for auth
    'django.contrib.messages.middleware.MessageMiddleware',  # Needed for messages
    #x'django.middleware.clickjacking.XContentOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Corrected middleware

]

# Static files configuration
STATIC_URL = '/static/'

# Pointing to the entire frontend folder (css, js, assets)
STATICFILES_DIRS = [
    BASE_DIR / 'frontend',  # Corrected to directly reference the frontend folder
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Directory where static files will be collected (for production)

# Default auto field configuration for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = ['*']  # Allow all hosts for now (this should be more restrictive in production)
