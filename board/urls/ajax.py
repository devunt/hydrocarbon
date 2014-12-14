from django.conf.urls import patterns, url, include

from board.views import VoteView


urlpatterns = patterns('',
    url(r'^v$', VoteView.as_view(), name='ajax_vote'),
)
