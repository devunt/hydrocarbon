from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.utils.functional import curry
from django.views.defaults import bad_request, page_not_found, permission_denied, server_error

from board.views import HCLoginView, HCSettingsView, HCSignupView
from board.views import CSSConstantsView, EmailConfirmationResendView, IndexView, JSConstantsView, NotificationView, PostListByTagView


urlpatterns = [
    url(r'^account/login/$', HCLoginView.as_view(), name='account_login'),
    url(r'^account/signup/$', HCSignupView.as_view(), name='account_signup'),
    url(r'^account/settings/$', HCSettingsView.as_view(), name='account_settings'),
    url(r'^account/email/resend/$', EmailConfirmationResendView.as_view(), name='account_resend_confirmation_email'),

    url(r'^account/', include('account.urls')),
    url(r'^search/', include('haystack.urls')),

    url(r'^constants.css$', CSSConstantsView.as_view(), name='constants.css'),
    url(r'^constants.js$', JSConstantsView.as_view(), name='constants.js'),
    url(r'^notifications$', NotificationView.as_view(), name='notification'),
    url(r'^t/(?P<tag>.+)/', PostListByTagView.as_view(), name='post_list_by_tag'),
    url(r'^x/', include('board.urls.ajax')),
    url(r'^u/(?P<user>\d+)/', include('board.urls.user')),
    url(r'^b/(?P<board>\w+)/', include('board.urls.board')),
    url(r'^(?P<pk>\d+)/', include('board.urls.post')),
    url(r'^$', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = curry(bad_request, template_name='errors/400.html')
handler403 = curry(permission_denied, template_name='errors/403.html')
handler404 = curry(page_not_found, template_name='errors/404.html')
handler500 = curry(server_error, template_name='errors/500.html')
