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
)

# Template context processor definition
TEMPLATE_CONTEXT_PROCESSORS = (
    'board.context_processors.current_url',
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

# Account urls
LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'account_login'
LOGOUT_URL = 'account_logout'

# Password encryption method
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

# E-email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@herocomics.kr'
EMAIL_HOST_PASSWORD = None # WILL BE OVERRIDED IN PRIVATE SETTINGS
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

# django-froala-editor
FROALA_INCLUDE_JQUERY = False
FROALA_EDITOR_PLUGINS = ('file_upload', 'lists', 'video', 'spoiler', 'icon_fix')
FROALA_EDITOR_OPTIONS = {
    'language': 'ko',
    'buttons': ['bold', 'italic', 'underline', 'spoiler',
                'formatBlock', 'align', 'insertOrderedList', 'insertUnorderedList',
                'createLink', 'insertImage', 'insertVideo', 'uploadFile', 'html'
    ],
    'inlineMode': False,
    'alwaysBlank': True,
    'imageUpload': True,
    'imageUploadURL': '/x/f',
    'imageUploadParams': {'type': 'i'},
    'fileUploadURL': '/x/f',
    'fileUploadParams': {'type': 'f'},
    'defaultImageWidth': 0,
    'linkAutoPrefix': 'http://',
}
FROALA_EDITOR_OPTIONS_COMMENT = FROALA_EDITOR_OPTIONS.copy()
FROALA_EDITOR_OPTIONS_COMMENT.update({
    'placeholder': _('Press ctrl-enter to submit a comment'),
})

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
def _filter_a_attr(name, value):
    if name in ('data-fr-link', 'href', 'rel', 'target'):
        return True
    if name == 'class' and value == 'fr-file':
        return True
    return False

def _filter_iframe_attr(name, value):
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

def _filter_img_attr(name, value):
    if name in ('alt', 'style', 'src', 'width'):
        return True
    if name == 'class':
        classes = value.split(' ')
        if set(classes) <= {'fr-image-move', 'fr-tag', 'fr-fil', 'fr-fin', 'fr-fir'}:
            return True
    return False

def _filter_span_attr(name, value):
    if name == 'class':
        classes = value.split(' ')
        if set(classes) <= {'f-video-editor', 'fr-fvl', 'fr-fvn', 'fr-fvr', 'spoiler'}:
            return True
    return False

BLEACH_ALLOWED_TAGS = [
    'blockquote', 'br', 'p', 'pre', 'span',
    'b', 'em', 'i', 'strike', 'strong', 'u',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'li', 'ol', 'ul',
    'a', 'img', 'iframe',
]
BLEACH_ALLOWED_ATTRIBUTES = {
    'a': _filter_a_attr,
    'iframe': _filter_iframe_attr,
    'img': _filter_img_attr,
    'p': ['style'],
    'span': _filter_span_attr,
}
BLEACH_ALLOWED_STYLES = [
    'display',
    'width', 'height',
    'margin', 'margin-left',
    'text-align',
]

# App settings
BOARD_COMMENT_MAX_DEPTH = 7

# Private settings override
try:
    from hydrocarbon.settings.private.base import *
except:
    pass
