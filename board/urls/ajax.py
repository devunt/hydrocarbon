from django.conf.urls import patterns, url

from board.views import CommentAjaxView, FileUploadAjaxView, NotificationAjaxView, TagAutocompleteAjaxView, VoteAjaxView


urlpatterns = patterns('',
    url(r'^v$', VoteAjaxView.as_view(), name='ajax_vote'),
    url(r'^c/(?P<pk>\d+)$', CommentAjaxView.as_view(), name='ajax_comment'),
    url(r'^t$', TagAutocompleteAjaxView.as_view(), name='ajax_tagautocomplete'),
    url(r'^f$', FileUploadAjaxView.as_view(), name='ajax_fileupload'),
    url(r'^n$', NotificationAjaxView.as_view(), name='ajax_notification'),
)
