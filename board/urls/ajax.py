from django.conf.urls import patterns, url, include

from board.views import CommentAjaxView, FileUploadAjaxView, VoteAjaxView


urlpatterns = patterns('',
    url(r'^v$', VoteAjaxView.as_view(), name='ajax_vote'),
    url(r'^f$', FileUploadAjaxView.as_view(), name='ajax_file_upload'),
    url(r'^c/(?P<pk>\d+)$', CommentAjaxView.as_view(), name='ajax_comment'),
)
