"""
Django settings for herbie project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

env = environ.Env()

# Business entity application label
APP_LABEL = 'herbieapp'

# Json schema package for validation of business objects
SCHEMA_REGISTRY_PACKAGE = 'herbie_json_schema'

# chunk size for exporting data
DEFAULT_CHUNK_SIZE = 100

# message_provider (e.g. kafka, google pubsub)
MESSAGING_PROVIDER = 'google_pub_sub'

# Google Cloud Pub/Sub
GCLOUD_PUBSUB_PROJECT_ID = env.str('GCLOUD_PUBSUB_PROJECT_ID', " ")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

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
    'rest_framework',
    'herbieapp.apps.HerbieappConfig',
    'rest_framework.authtoken',
    'social_django'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware'
]

ROOT_URLCONF = 'herbie.urls'


SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'herbieapp.authentication.social_authentication.process_roles'
)


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/admin'

SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]


WSGI_APPLICATION = 'herbie.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'kafka': {
            'handlers': ['console'],
            'level': 'WARNING'
        },
    }
}

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

JSON_VIEWER = {
    'JS_URL': 'json-viewer/jquery.json-viewer.js',
    'CSS_URL': 'json-viewer/jquery.json-viewer.css'
}

HERBIE_ADMIN = {
    'JS_URL': 'js/herbie-admin.js',
    'CSS_URL': 'css/herbie-admin.css',
}

KAFKA = {
    'SERVERS': 'herbie-kafka:9093',
    'TIMEOUT': 30000
}
