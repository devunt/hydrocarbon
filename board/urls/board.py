from django.conf.urls import patterns, url, include

from board.views import PostCreateView, PostListView


urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='board_post_list'),
    url(r'^newpost/$', PostCreateView.as_view(), name='board_post_create'),
)
