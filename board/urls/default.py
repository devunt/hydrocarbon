from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.utils.functional import curry
from django.views.defaults import permission_denied

from board.views import HCLoginView, HCSignupView, IndexView


urlpatterns = patterns('',
    url(r'^account/login/$', HCLoginView.as_view(), name='account_login'),
    url(r'^account/signup/$', HCSignupView.as_view(), name='account_signup'),
    url(r'^account/', include('account.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^redactor/', include('redactor.urls')),

    url(r'^x/', include('board.urls.ajax')),
    url(r'^b/(?P<board>\w+)/', include('board.urls.board')),
    url(r'^(?P<pk>\d+)/', include('board.urls.post')),
    url(r'^$', IndexView.as_view()),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = curry(permission_denied, template_name='errors/403.html')
