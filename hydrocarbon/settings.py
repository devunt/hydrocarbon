"""
Django settings for hydrocarbon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yw-x*phaeqr%i0og#%$lccg@77h7dbw786yu8vu(#6f#a_m4e7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

SITE_ID = 1


# Application definition
INSTALLED_APPS = (
    # local apps
    'board',
    ) + (
    # third-party apps
    'registration',
    'django_summernote',
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
)

ROOT_URLCONF = 'hydrocarbon.urls'

WSGI_APPLICATION = 'hydrocarbon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Template
TEMPLATE_CONTEXT_PROCESSORS = (
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

# django-registration-redux
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# django-summernote
SUMMERNOTE_CONFIG = {
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'underline', 'strikethrough', 'clear']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['insert', ['picture', 'link']],
        ['misc', ['codeview']]
    ],
    'inplacewidget_external_css': (
        '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
}

# App settings
BOARD_POST_BEST_VOTES = 1
LOGIN_REDIRECT_URL = '/'
