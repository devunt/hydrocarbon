from django.conf.urls import patterns, url

from board.views import PostCreateView, PostListView, PostBestListView


urlpatterns = patterns('',
    url(r'^(?P<order_by>[+-][a-z]{2})?$', PostListView.as_view(), name='board_post_list'),
    url(r'^best/(?P<order_by>[+-][a-z]{2})?$', PostBestListView.as_view(), name='board_post_list_best'),
    url(r'^newpost/$', PostCreateView.as_view(), name='board_post_create'),
)
