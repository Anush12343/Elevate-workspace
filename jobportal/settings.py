from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-&5fa((y6$hz#y2x+fr&!*(t-&0f(#n&!^y$z^+76fh^&u7#a&#'

import os
import sys

# ✅ Set DEBUG dynamically: True for local development, False for production (PythonAnywhere)
DEBUG = 'runserver' in sys.argv or 'test' in sys.argv or os.environ.get('DJANGO_DEVELOPMENT', 'False').lower() == 'true'

# ✅ Add your PythonAnywhere username below (replace 'yourusername')
ALLOWED_HOSTS = ['RYzen.pythonanywhere.com', '127.0.0.1', 'localhost', 'testserver']

# ✅ Required for Django 4.0+ to prevent CSRF failures on HTTPS production sites
CSRF_TRUSTED_ORIGINS = ['https://RYzen.pythonanywhere.com', 'http://RYzen.pythonanywhere.com']

# ✅ FIXED: Single INSTALLED_APPS with 'jobs' included
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobs',  # Your app
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

ROOT_URLCONF = 'jobportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ Correct
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'jobs.context_processors.user_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'jobportal.wsgi.application'

# 🗄️ DATABASE: SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'  # ✅ Nepal timezone
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ✅ Required for collectstatic on PythonAnywhere
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Media files for CV uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Authentication redirects
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
