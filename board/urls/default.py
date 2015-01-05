from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.utils.functional import curry
from django.views.defaults import permission_denied
from redactor.forms import FileForm, ImageForm

from board.views import HCLoginView, HCSettingsView, HCSignupView, HCRedactorUploadView
from board.views import IndexView, JSConstantsView, PostListByTagView


urlpatterns = patterns('',
    url(r'^account/login/$', HCLoginView.as_view(), name='account_login'),
    url(r'^account/signup/$', HCSignupView.as_view(), name='account_signup'),
    url(r'^account/settings/$', HCSettingsView.as_view(), name='account_settings'),
    url(r'^redactor/upload/image/(?P<upload_to>.*)',
        HCRedactorUploadView.as_view(form_class=ImageForm),
        name='redactor_upload_image'),
    url(r'^redactor/upload/file/(?P<upload_to>.*)',
        HCRedactorUploadView.as_view(form_class=FileForm),
        name='redactor_upload_file'),

    url(r'^account/', include('account.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^redactor/', include('redactor.urls')),

    url(r'^constants.js', JSConstantsView.as_view(), name='constants.js'),
    url(r'^t/(?P<tag>\w+)/', PostListByTagView.as_view(), name='post_list_by_tag'),
    url(r'^x/', include('board.urls.ajax')),
    url(r'^u/(?P<user>\d+)/', include('board.urls.user')),
    url(r'^b/(?P<board>\w+)/', include('board.urls.board')),
    url(r'^(?P<pk>\d+)/', include('board.urls.post')),
    url(r'^$', IndexView.as_view()),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = curry(permission_denied, template_name='errors/403.html')
