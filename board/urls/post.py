from django.conf.urls import patterns, url, include

from board.views import PostDeleteView, PostDetailView, PostUpdateView


urlpatterns = patterns('',
    url(r'^$', PostDetailView.as_view(), name='post_detail'),
    url(r'^modify$', PostUpdateView.as_view(), name='post_update'),
    url(r'^delete$', PostDeleteView.as_view(), name='post_delete'),
)
