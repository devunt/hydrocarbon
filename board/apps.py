import django

from django.apps import AppConfig
from django.conf import settings

from board.pagination import HCPaginator


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = 'hydrocarbon board'

    def ready(self):
        import board.signals
        django.core.paginator.Paginator = HCPaginator
        settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'] = str(settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'])
