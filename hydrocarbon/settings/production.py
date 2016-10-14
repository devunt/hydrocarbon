from hydrocarbon.settings.base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None # WILL BE OVERRIDED IN PRIVATE SETTINGS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# ALLOWED HOSTS
ALLOWED_HOSTS = ['herocomics.kr']

# Installed apps
INSTALLED_APPS += (
    'celery_haystack',
    'raven.contrib.django.raven_compat',
)

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
        'PASSWORD': None, # WILL BE OVERRIDED IN PRIVATE SETTINGS
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': False,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = '/home/herocomics/static'
STATIC_URL = 'http://s.herocomics.kr/'

# Media files
MEDIA_ROOT = '/home/herocomics/media'
MEDIA_URL = 'http://uc.herocomics.kr/'

# django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'board.backends.ConfigurableElasticSearchEngine',
        'URL': '127.0.0.1:9200',
        'TIMEOUT': 300,
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'
SEARCH_INDEX_CLASS = 'celery_haystack.indexes.CelerySearchIndex'
ELASTICSEARCH_INDEX_SETTINGS = {
    'settings': {
        'index': {
            'analysis': {
                'analyzer': {
                    'hydrocarbon': {
                        'type': 'custom',
                        'char_filter': 'html_strip',
                        'tokenizer': 'korean_query_tokenizer',
                        'filter': 'trim',
                    },
                },
                'tokenizer': {
                    'korean_query_tokenizer': {
                        'type': 'mecab_ko_standard_tokenizer',
                        'mecab_dic_dir': '/opt/mecab-ko/lib/mecab/dic/mecab-ko-dic/',
                    },
                },
            },
        },
    },
}
ELASTICSEARCH_DEFAULT_ANALYZER = 'hydrocarbon'

# Raven settings
RAVEN_CONFIG = {
    'dsn': None, # WILL BE OVERRIDED IN PRIVATE SETTINGS
}

# App settings
BOARD_POST_BLIND_VOTES = -10
BOARD_POST_BEST_VOTES = 10
BOARD_COMMENT_BLIND_VOTES = -5

# Private settings override
from hydrocarbon.settings.private.production import *
DATABASES['default']['PASSWORD'] = DATABASES_PASSWORD
FROALA_EDITOR_OPTIONS['key'] = FROALA_ACTIVATION_KEY
FROALA_EDITOR_OPTIONS_COMMENT['key'] = FROALA_ACTIVATION_KEY
RAVEN_CONFIG['dsn'] = RAVEN_CONFIG_DSN
