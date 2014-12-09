from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail


class HCRegistrationForm(RegistrationFormUniqueEmail):
    nick = forms.CharField(label=_('Nickname:'), min_length=2, max_length=16)
