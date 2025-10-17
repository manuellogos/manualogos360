import os
import dj_database_url
from .base import *

DEBUG = False

# Hosts permitidos para Render
ALLOWED_HOSTS = [
    'manualogos360.onrender.com',
    '*.onrender.com',
    'localhost',
    '127.0.0.1'
]

# Middleware con WhiteNoise para archivos estáticos
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# Base de datos para producción (PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

# Archivos estáticos - Configuración con WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Prefer using STORAGES (Django 4.2+) so it overrides base.STORAGES safely.
# Avoid Manifest storage in production until the collectstatic output is stable,
# because missing manifest entries raise runtime errors (we saw favicon errors).
# Use WhiteNoise's compressed storage (no manifest) so files are served from
# STATIC_ROOT without manifest enforcement.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

# WhiteNoise runtime options - disable autoreload in production
WHITENOISE_USE_FINDERS = False
WHITENOISE_AUTOREFRESH = False

# Archivos de media (imágenes subidas)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Secret key desde variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# Base URL de Wagtail para producción
WAGTAILADMIN_BASE_URL = 'https://manualogos360.onrender.com'

# Configuración de seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging mejorado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.staticfiles': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
