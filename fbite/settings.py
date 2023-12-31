"""
Django settings for fbite project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import logging
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-eaf4e8_%072ix29-q5-mg8q=-tm03lb-8p&k^@yy&su0=$p)ie'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'firebase_admin',
    'celery',
    'drf_yasg',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    'AULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Firebase Authentication Configuration
FIREBASE_AUTH = {
    "SERVICE_ACCOUNT_KEY_FILE": os.path.join(BASE_DIR, "firebase/credentials.json"),
    "EMAIL_VERIFICATION": False,  # require that user has verified their email
}

ROOT_URLCONF = 'fbite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fbite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuração do logger
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ----Configuração do backend de e-mail----

# Define o backend de e-mail que será utilizado pelo Django.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Define o endereço do servidor SMTP que será usado para enviar e-mails.
EMAIL_HOST = 'smtp.gmail.com'

# Define a porta do servidor SMTP que será usada para enviar e-mails.
EMAIL_PORT = 587

# Define o nome de usuário da conta de e-mail que será usada para enviar os e-mails.
EMAIL_HOST_USER = 'mathkol@sempreceub.com'

# Define a senha da conta de e-mail que será usada para enviar os e-mails.
EMAIL_HOST_PASSWORD = 'Reidobode123'

# Define se a comunicação com o servidor SMTP será feita usando TLS.
EMAIL_USE_TLS = True

# Define se a comunicação com o servidor SMTP será feita usando SSL.
EMAIL_USE_SSL = False

# ----Configuração do backend de e-mail----

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = STATIC_URL = '/static/'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'social_core.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'atualizar-estoque': {
        'task': 'main.tasks.atualizar_estoque',
        'schedule': 60.0,
    },
}

# Twilio config
TWILIO_SID = 'AC63fd3b75a008ba09cc72f43c15ac2e35'
TWILIO_AUTH_TOKEN = "9937da2e5cb370d0ec1e441dc45cdefd"
TWILIO_PHONE_NUMBER = "+15418626916"
