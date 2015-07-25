import django

from django.apps import AppConfig
from django.conf import settings
from importlib import import_module

from board.pagination import HCPaginator


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = 'hydrocarbon board'

    def ready(self):
        import board.signals
        django.core.paginator.Paginator = HCPaginator
        settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'] = str(settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'])
        module, cls = settings.SEARCH_INDEX_CLASS.rsplit('.', maxsplit=1)
        module = import_module(module)
        settings.SEARCH_INDEX_CLASS = getattr(module, cls)
