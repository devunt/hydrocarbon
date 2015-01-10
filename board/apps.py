from django.apps import AppConfig
from django.conf import settings


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = 'hydrocarbon board'

    def ready(self):
        import board.signals
        settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'] = str(settings.FROALA_EDITOR_OPTIONS_COMMENT['placeholder'])
