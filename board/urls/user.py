from django.conf.urls import patterns, url

from board.views import UserProfileView, UserPostListView, UserCommentListView


urlpatterns = patterns('',
    url(r'^$', UserProfileView.as_view(), name='user_profile'),
    url(r'^posts/$', UserPostListView.as_view(), name='user_profile_posts'),
    url(r'^comments/$', UserCommentListView.as_view(), name='user_profile_comments'),
)
