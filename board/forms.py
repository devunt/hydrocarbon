from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from redactor.widgets import RedactorEditor
from registration.forms import RegistrationFormUniqueEmail

from board.models import Category, Comment, Post, Tag


class ModelCommaSeparatedChoiceField(forms.ModelMultipleChoiceField):
    widget = TextInput

    def prepare_value(self, value):
        lst = list()
        if isinstance(value, list):
            for item in value:
                lst.append(getattr(self.queryset.get(id=item), self.to_field_name))
            value = ', '.join(lst)
        return super().prepare_value(value)

    def clean(self, value):
        if value not in ('', None):
            lst = list()
            for item in value.split(','):
                item = item.strip()
                if item == '':
                    continue
                kwargs = {self.to_field_name: item}
                if not self.queryset.filter(**kwargs).exists():
                    t = Tag()
                    t.name = item
                    t.save()
                lst.append(item)
            value = lst
        return super().clean(value)


class HCRegistrationForm(RegistrationFormUniqueEmail):
    nick = forms.CharField(label=_('Nickname'), min_length=2, max_length=16)


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None)
    tags = ModelCommaSeparatedChoiceField(queryset=Tag.objects.all(), to_field_name='name', required=False)

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
        labels = {
            'contents': '',
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        authenticated = kwargs.pop('authenticated')
        super().__init__(*args, **kwargs)
        if not authenticated:
            self.fields['onetime_nick'] = forms.CharField(label=_('Nickname'), max_length=16)
            self.fields['onetime_password'] = forms.CharField(label=_('Password'), widget=forms.PasswordInput())

    class Meta:
        model = Comment
        fields = ['contents']
        labels = {
            'contents': '',
        }
        widgets = {
            'contents': RedactorEditor(
                redactor_options={'placeholder': _('Press ctrl-enter to submit a comment')},
            ),
        }


class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
