import django

from django.apps import AppConfig
from django.conf import settings

from board.pagination import HCPaginator


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = 'hydrocarbon board'

    def ready(self):
        import board.signals
        settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholderText'] = str(settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholderText'])
