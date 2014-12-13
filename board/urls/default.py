from django.conf.urls import patterns, url, include
from registration.backends.default.views import RegistrationView

from board.forms import HCRegistrationForm


urlpatterns = patterns('',
    url(r'^accounts/register/$',
        RegistrationView.as_view(form_class=HCRegistrationForm),
        name='registration_register'
    ),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^x/', include('board.urls.ajax')),
    url(r'^b/(?P<board>\w+)/', include('board.urls.board')),
    url(r'^(?P<pk>\d+)/?', include('board.urls.post')),
)
