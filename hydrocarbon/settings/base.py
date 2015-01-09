"""
Django settings for hydrocarbon project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
from urllib.parse import urlparse
from django.utils.translation import ugettext_lazy as _


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.normpath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))

# Default site id
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
    'froala_editor',
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

# Middleware definition
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

# Template context processor definition
TEMPLATE_CONTEXT_PROCESSORS = (
    'board.context_processors.current_url',
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

# Authentication backends
AUTH_USER_MODEL = 'board.User'
AUTHENTICATION_BACKENDS = (
    'account.auth_backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Password encryption method
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

# E-email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@herocomics.kr'
EMAIL_HOST_PASSWORD = '***REMOVED***'
DEFAULT_FROM_EMAIL = 'no-reply@herocomics.kr'

# Various settings
ROOT_URLCONF = 'hydrocarbon.urls'
WSGI_APPLICATION = 'hydrocarbon.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
LANGUAGES = (
    ('ko', _('Korean')),
)
LANGUAGE_CODE = 'ko-kr'

USE_I18N = True
USE_L10N = True

TIME_ZONE = 'Asia/Seoul'
USE_TZ = True

# django-user-accounts
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE = False
ACCOUNT_DELETION_MARK_CALLBACK = 'board.callbacks.account_delete_mark'
ACCOUNT_DELETION_EXPUNGE_CALLBACK = 'board.callbacks.account_delete_expunge'

# django-wysiwyg-redactor
REDACTOR_OPTIONS = {'lang': 'ko', 'toolbarFixed': False, 'tabKey': False, 'buttonsHide': ['horizontalrule'], 'plugins': ['video', 'spoiler', 'krfix', 'autosave_garlic']}
REDACTOR_UPLOAD = 'uploads/'
REDACTOR_UPLOAD_HANDLER = 'redactor.handlers.DateDirectoryUploader'

# django-froala-editor
FROALA_INCLUDE_JQUERY = False
FROALA_EDITOR_PLUGINS = ('file_upload', 'lists', 'video')
FROALA_EDITOR_OPTIONS = {
    'language': 'ko',
    'buttons': ['bold', 'italic', 'underline', 'strikeThrough',
                'formatBlock', 'align', 'insertOrderedList', 'insertUnorderedList',
                'createLink', 'insertImage', 'insertVideo', 'uploadFile', 'html'
    ],
    'alwaysBlank': True,
}

# django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'board.backends.ConfigurableElasticSearchEngine',
        'URL': '127.0.0.1:9200',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# bleach
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

# App settings
BOARD_COMMENT_MAX_DEPTH = 4
