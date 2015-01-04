from django.conf.urls import patterns, url

from board.views import UserProfileView, UserPostListView


urlpatterns = patterns('',
    url(r'^$', UserProfileView.as_view(), name='user_profile'),
    url(r'^posts/$', UserPostListView.as_view(), name='user_profile_posts'),
)
