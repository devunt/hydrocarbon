from django.conf.urls import patterns, url, include
from registration.backends.simple.views import RegistrationView

from board.forms import HCRegistrationForm


urlpatterns = patterns('',
    url(r'^accounts/register/$',
        RegistrationView.as_view(form_class=HCRegistrationForm),
        name='registration_register'
    ),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)
