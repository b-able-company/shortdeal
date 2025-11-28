"""
Django local development settings for ShortDeal project.
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database - PostgreSQL (Docker)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shortdeal',
        'USER': 'shortdeal',
        'PASSWORD': os.getenv('DB_PASSWORD', 'shortdeal123'),
        'HOST': 'db',  # Docker DB accessed from local host
        'PORT': '5432',
    }
}

# Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']

# Email - 콘솔 출력 (개발용)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 로깅
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
}
