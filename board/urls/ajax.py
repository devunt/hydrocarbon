from django.conf.urls import patterns, url, include

from board.views import RecommendView


urlpatterns = patterns('',
    url(r'^r$', RecommendView.as_view(), name='recommend'),
)
