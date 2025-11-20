"""
Django settings for hospitalmanagement project.
Hard-coded PostgreSQL URL for local testing.
"""

import os
import dj_database_url

# ------------------------------------------------------------------
# Build paths
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# ------------------------------------------------------------------
# Security
# ------------------------------------------------------------------
SECRET_KEY = 'hpbv()ep00boce&o0w7z1h)st148(*m@6@-rk$nn)(n9ojj4c0'  # change in prod
DEBUG = True  # set False on Render
# Add this line anywhere in settings.py
RENDER = True  # This tells your code you're on Render

ALLOWED_HOSTS = ['*']  # tighten on Render: ['your-app.onrender.com']

# ------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hospital',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospitalmanagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'hospitalmanagement.wsgi.application'

# ------------------------------------------------------------------
# DATABASE – HARD-CODED FOR LOCAL TESTING
# ------------------------------------------------------------------
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://chl:V10qloYppfydmirjiTHGVhm3CqCaKd7J@dpg-d41l7dre5dus73de6vig-a.oregon-postgres.render.com/chl?sslmode=require',
        conn_max_age=600,
        conn_health_checks=True
    )
}

# ------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------
LOGIN_REDIRECT_URL = '/afterlogin'

# ------------------------------------------------------------------
# Email (local testing – use your own)
# ------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'from@gmail.com'
EMAIL_HOST_PASSWORD = ''  # fill in locally
EMAIL_RECEIVING_USER = ['to@gmail.com']

# ------------------------------------------------------------------
# Default primary key
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'