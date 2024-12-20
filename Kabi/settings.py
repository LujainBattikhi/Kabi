"""
Django settings for Kabi project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from celery.schedules import crontab
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$=!14(s-bec4n@n8z*s7eb!f301mvuk-cmy6rngkfqc-gp9%s+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '172.20.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'Kabi.apps.accounts',
    'Kabi.apps.jobs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kabi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


WSGI_APPLICATION = 'Kabi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = config("STATIC_URL", '/static/')
STATIC_ROOT = config("STATIC_ROOT", os.path.join(BASE_DIR, 'statics'))

MEDIA_URL = config("MEDIA_URL", '/media/')
MEDIA_ROOT = config("MEDIA_ROOT", os.path.join(BASE_DIR, 'media'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/accounts/login/'          # Redirect here if login is required
LOGIN_REDIRECT_URL = '/'                # Redirect here after successful login
LOGOUT_REDIRECT_URL = '/accounts/login/' # Redirect here after logout


# Celery Configuration Options

CELERY_BROKER_URL = 'redis://kabi-redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Celery Beat settings (optional, if needed)
CELERY_BEAT_SCHEDULE = {
    'health_checker': {
        'task': 'Kabi.apps.jobs.tasks.health_checker',
        'schedule': crontab(minute='*/30'),
    },
    'test_task': {
        'task': 'Kabi.apps.jobs.tasks.load_jobs',
        'schedule': crontab(hour='0', minute='0'),
    },
}

LOGS_PATH = config('LOGS_PATH', '')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'activity': {
            'class': 'logging.FileHandler',
            'filename': LOGS_PATH + 'activity_logs.log',
        },
        'rotator': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_PATH + 'server_logs.log',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
    },
    'loggers': {
        'activity': {
            'handlers': ['activity', 'console'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django': {
            'handlers': ['console', 'rotator'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'celery': {
            'handlers': ['console', 'rotator'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'Kabi': {
            'handlers': ['console', 'rotator'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'django.db': {
            'handlers': ['console', 'rotator'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
