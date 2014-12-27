from django.conf.urls import patterns, url, include

from board.views import CommentAjaxView, VoteAjaxView


urlpatterns = patterns('',
    url(r'^v$', VoteAjaxView.as_view(), name='ajax_vote'),
    url(r'^c/(?P<pk>\d+)$', CommentAjaxView.as_view(), name='ajax_comment'),
)
