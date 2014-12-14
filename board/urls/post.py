from django.conf.urls import patterns, url, include

from board.views import PostDetailView, PostUpdateView


urlpatterns = patterns('',
    url(r'^$', PostDetailView.as_view(), name='post_detail'),
    url(r'^modify$', PostUpdateView.as_view(), name='post_update'),
)
