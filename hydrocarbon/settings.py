"""
Django settings for hydrocarbon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from urllib.parse import urlparse
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yw-x*phaeqr%i0og#%$lccg@77h7dbw786yu8vu(#6f#a_m4e7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['herocomics.kr', '127.0.0.1']

SITE_ID = 1


# Application definition
INSTALLED_APPS = (
    # local apps
    'board',
    ) + (
    # third-party apps
    'account',
    'custom_user',
    'redactor',
    'haystack',
    ) + (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'hydrocarbon.urls'

WSGI_APPLICATION = 'hydrocarbon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

# Template
TEMPLATE_CONTEXT_PROCESSORS = (
    'account.context_processors.account',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGES = (
    ('ko', _('Korean')),
    ('en', _('English')),
)

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'board/static')

STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'board/media')

MEDIA_URL = '/media/'

# User model
AUTH_USER_MODEL = 'board.User'

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'account.auth_backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password encryption method
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

# Session backend
SESSION_ENGINE = 'django.contrib.sessions.backends.file' # for debugging

# E-email
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.zoho.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'no-reply@herocomics.kr'

EMAIL_HOST_PASSWORD = '***REMOVED***'

DEFAULT_FROM_EMAIL = 'no-reply@herocomics.kr'

# django-user-accounts
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE = False

# django-wysiwyg-redactor
REDACTOR_OPTIONS = {'lang': 'ko', 'toolbarFixed': False, 'plugins': ['video', 'spoiler']}
REDACTOR_UPLOAD = 'uploads/'
REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.DateDirectoryUploader'

# django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '127.0.0.1:9200',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# App settings
BOARD_POST_BLIND_VOTES = -1 # DEBUGGING
BOARD_POST_BEST_VOTES = 1 # DEBUGGING
LOGIN_REDIRECT_URL = '/'

def _filter_iframe_src(name, value):
    if name in ('allowfullscreen', 'frameborder', 'height', 'style', 'width'):
        return True
    if name == 'src':
        p = urlparse(value)
        return p.netloc in (
            'youtube.com',
            'www.youtube.com',
            'youtube-nocookie.com',
            'www.youtube-nocookie.com',
        )
    return False

def _filter_span_class(name, value):
    if name == 'class' and value == 'spoiler':
        return True
    return False

BLEACH_ALLOWED_TAGS = [
    'blockquote', 'br', 'hr', 'p', 'pre', 'span',
    'del', 'em', 'strong',
    'h1', 'h2', 'h3', 'h4', 'h5',
    'li', 'ol', 'ul',
    'a', 'img', 'iframe',
]
BLEACH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target'],
    'iframe': _filter_iframe_src,
    'img': ['alt', 'style', 'src'],
    'p': ['style'],
    'span': _filter_span_class,
}
BLEACH_ALLOWED_STYLES = [
    'display',
    'width', 'height',
    'margin', 'margin-left',
    'text-align',
]
