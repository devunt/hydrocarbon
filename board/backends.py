from django.conf import settings
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine


class ConfigurableElasticBackend(ElasticsearchSearchBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS', False)
        if user_settings:
            setattr(self, 'DEFAULT_SETTINGS', user_settings)


class ConfigurableElasticSearchEngine(ElasticsearchSearchEngine):
    backend = ConfigurableElasticBackend
