import os

from hydrocarbon.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# ALLOWED HOSTS
ALLOWED_HOSTS = ['herocomics.kr', 'beta.herocomics.kr']

# Cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '10.54.45.1:11211',
    }
}

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hydrocarbon',
        'USER': 'herocomics',
        'PASSWORD': '***REMOVED***',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    }
}

# Template loaders
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = '/home/herocomics/static'
STATIC_URL = 'http://s.herocomics.kr/'

# Media files
MEDIA_ROOT = '/home/herocomics/media'
MEDIA_URL = 'http://uc.herocomics.kr/'
