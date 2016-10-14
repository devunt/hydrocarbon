from django.conf.urls import url

from board.views import PostDeleteView, PostDetailView, PostUpdateView


urlpatterns = [
    url(r'^$', PostDetailView.as_view(), name='post_detail'),
    url(r'^modify$', PostUpdateView.as_view(), name='post_update'),
    url(r'^delete$', PostDeleteView.as_view(), name='post_delete'),
]
