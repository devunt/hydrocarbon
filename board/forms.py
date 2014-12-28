from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from redactor.widgets import RedactorEditor
from registration.forms import RegistrationFormUniqueEmail

from board.models import Category, Post


class HCRegistrationForm(RegistrationFormUniqueEmail):
    nick = forms.CharField(label=_('Nickname'), min_length=2, max_length=16)


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        authenticated = kwargs.pop('authenticated')
        board = kwargs.pop('board')
        super().__init__(*args, **kwargs)
        cqs = Category.objects.filter(board=board)
        self.fields['category'].queryset = cqs
        if not cqs.exists():
            del self.fields['category']
        if not authenticated:
            self.fields['onetime_nick'] = forms.CharField(label=_('Nickname'), max_length=16)
            self.fields['onetime_password'] = forms.CharField(label=_('Password'), widget=forms.PasswordInput())

    class Meta:
        model = Post
        fields = ['category', 'title', 'contents', 'tags']
        widgets = {
            'contents': RedactorEditor(),
            'tags': TextInput(),
        }
        labels = {
            'contents': '',
        }


class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
