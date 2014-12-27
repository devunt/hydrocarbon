from django.conf.urls import patterns, url

from board.views import PostCreateView, PostListView, PostBestListView


urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='board_post_list'),
    url(r'^best/$', PostBestListView.as_view(), name='board_post_list_best'),
    url(r'^newpost/$', PostCreateView.as_view(), name='board_post_create'),
)
