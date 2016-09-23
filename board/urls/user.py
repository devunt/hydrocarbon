from django.conf.urls import url

from board.views import UserProfileView, UserPostListView, UserCommentListView


urlpatterns = [
    url(r'^$', UserProfileView.as_view(), name='user_profile'),
    url(r'^posts/$', UserPostListView.as_view(), name='user_profile_posts'),
    url(r'^comments/$', UserCommentListView.as_view(), name='user_profile_comments'),
]
