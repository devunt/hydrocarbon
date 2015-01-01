from collections import OrderedDict

from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from account.forms import LoginEmailForm, SignupForm
from redactor.widgets import RedactorEditor

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


class HCLoginForm(LoginEmailForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class HCSignupForm(SignupForm):
    nickname = forms.CharField(label=_('Nickname'), min_length=2, max_length=16)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
        order = ('email', 'password', 'password_confirm', 'nickname', 'code')
        self.fields = OrderedDict((k, self.fields[k]) for k in order)

    def clean_nickname(self):
        value = self.cleaned_data['nickname']
        qs = get_user_model().objects.filter(nickname__iexact=value)
        if not qs.exists():
            return self.cleaned_data['nickname']
        raise forms.ValidationError(_('This nickname is already taken. Please choose another.'))


class OneTimeUserFormMixin:
    def __init__(self, *args, **kwargs):
        self.authenticated = kwargs.pop('authenticated')
        super().__init__(*args, **kwargs)
        if not self.authenticated:
            self.fields['onetime_nick'] = forms.CharField(label=_('Nickname'), max_length=16)
            self.fields['onetime_password'] = forms.CharField(label=_('Password'), widget=forms.PasswordInput())


class PostForm(OneTimeUserFormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None)
    tags = ModelCommaSeparatedChoiceField(queryset=Tag.objects.all(), to_field_name='name', required=False)

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board')
        super().__init__(*args, **kwargs)
        cqs = Category.objects.filter(board=board)
        self.fields['category'].queryset = cqs
        if not cqs.exists():
            del self.fields['category']

    class Meta:
        model = Post
        fields = ['category', 'title', 'contents', 'tags']
        labels = {
            'contents': '',
        }


class CommentForm(OneTimeUserFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']
        labels = {
            'contents': '',
        }
        widgets = {
            'contents': RedactorEditor(
                redactor_options={'placeholder': _('Press ctrl-space to submit a comment')},
            ),
        }


class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
