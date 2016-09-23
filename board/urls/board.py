from django.conf.urls import url

from board.views import BoardSearchView, PostCreateView, PostListView, PostBestListView, PostListByCategoryView


urlpatterns = [
    url(r'^$', PostListView.as_view(), name='board_post_list'),
    url(r'^best/$', PostBestListView.as_view(), name='board_post_list_best'),
    url(r'^c/(?P<category>\w+)/$', PostListByCategoryView.as_view(), name='board_post_list_by_category'),
    url(r'^search', BoardSearchView.as_view(), name='board_search'),
    url(r'^newpost/$', PostCreateView.as_view(), name='board_post_create'),
]
