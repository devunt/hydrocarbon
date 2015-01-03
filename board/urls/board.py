from django.conf.urls import patterns, url

from board.views import BoardSearchView, PostCreateView, PostListView, PostBestListView, PostListByCategoryView


urlpatterns = patterns('',
    url(r'^(?P<order_by>[+-][a-z]{2})?$', PostListView.as_view(), name='board_post_list'),
    url(r'^best/(?P<order_by>[+-][a-z]{2})?$', PostBestListView.as_view(), name='board_post_list_best'),
    url(r'^c/(?P<category>\w+)/$', PostListByCategoryView.as_view(), name='board_post_list_by_category'),
    url(r'^search', BoardSearchView.as_view(), name='board_search'),
    url(r'^newpost/$', PostCreateView.as_view(), name='board_post_create'),
)
