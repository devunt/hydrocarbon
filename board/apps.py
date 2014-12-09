from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'board'
    verbose_name = 'hydrocarbon board'

    def ready(self):
        import board.signals
