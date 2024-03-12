import os
from pathlib import Path
import sys

from configurations import Configuration
from configurations import values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = values.Value()

    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        # App locals
        'src.core.apps.CoreConfig',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'src.urls'

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

    WSGI_APPLICATION = 'src.wsgi.application'

    DATABASES = values.DatabaseURLValue('sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))

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

    LANGUAGE_CODE = values.Value('en-us')

    TIME_ZONE = values.Value('UTC')

    USE_I18N = values.BooleanValue(True)

    USE_TZ = values.BooleanValue(True)

    STATIC_URL = '/static/'

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STORAGES = {
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

    EMAIL = values.EmailURLValue('console://')

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    REST_FRAMEWORK = {'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'}

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d',
            },
        },
        'handlers': {
            'stdout': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'formatter': 'json',
            },
        },
        'loggers': {
            '': {
                'handlers': ['stdout'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


class Dev(Base):
    CACHES = values.CacheURLValue('dummy://')

    Base.INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')


class Prod(Base):
    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_SECURE = True
