from django.conf.urls import patterns, url, include

from board.views import PostDetailView


urlpatterns = patterns('',
    url(r'^$', PostDetailView.as_view(), name='post_detail'),
)
