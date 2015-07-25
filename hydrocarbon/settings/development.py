import os

from hydrocarbon.settings.base import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yw-x*phaeqr%i0og#%$lccg@77h7dbw786yu8vu(#6f#a_m4e7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# ALLOWED HOSTS
ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': False,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'board/static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'board/media')
MEDIA_URL = '/media/'

# django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
SEARCH_INDEX_CLASS = 'haystack.indexes.SearchIndex'

# App settings
BOARD_POST_BLIND_VOTES = -1
BOARD_POST_BEST_VOTES = 1
BOARD_COMMENT_BLIND_VOTES = -1
