from collections import OrderedDict

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from account.forms import LoginEmailForm, PasswordResetForm, SignupForm, SettingsForm
from account.models import EmailAddress
from captcha.fields import ReCaptchaField

from board.models import Category, Comment, Post, Tag
from board.utils import is_empty_html


def validate_contents(value):
    if is_empty_html(value):
        raise ValidationError(message='', code='required')

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


class OneTimeUserFormMixin:
    def __init__(self, *args, **kwargs):
        show_ot_form = kwargs.pop('show_ot_form', False)
        super().__init__(*args, **kwargs)
        if show_ot_form:
            self.fields['onetime_nick'] = forms.CharField(label=_('Nickname'), max_length=16)
            self.fields['onetime_password'] = forms.CharField(label=_('Password'), widget=forms.PasswordInput(render_value=True))
            self.fields['captcha'] = ReCaptchaField()


class NicknameFormMixin:
    nickname = forms.CharField(label=_('Nickname'), min_length=2, max_length=16)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'] = self.nickname

    def clean_nickname(self):
        value = self.cleaned_data['nickname'].strip()
        if self.initial.get('nickname') == value:
            return value
        qs = get_user_model().objects.filter(nickname__iexact=value)
        if not qs.exists():
            return value
        raise forms.ValidationError(_('This nickname is already taken. Please choose another.'))


class HCLoginForm(LoginEmailForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class HCSignupForm(NicknameFormMixin, SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']
        del self.fields['code']
        order = ('email', 'password', 'password_confirm', 'nickname')
        self.fields = OrderedDict((k, self.fields[k]) for k in order)
        self.fields['email'].widget = forms.EmailInput()


class HCSettingsForm(NicknameFormMixin, SettingsForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['timezone']
        del self.fields['language']


class EmailConfirmationResendForm(PasswordResetForm):
    def clean_email(self):
        value = super().clean_email()
        if EmailAddress.objects.get(email__iexact=value).verified:
            raise forms.ValidationError(_('This email address is already confirmed.'))
        return value


class PostForm(OneTimeUserFormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None)
    tags = ModelCommaSeparatedChoiceField(queryset=Tag.objects.all(), to_field_name='name', required=False)

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board')
        super().__init__(*args, **kwargs)
        cqs = Category.objects.filter(board=board)
        self.fields['category'].queryset = cqs
        self.fields['category'].initial = cqs.first()
        self.fields['contents'].validators.append(validate_contents)
        if not cqs.exists():
            del self.fields['category']

    class Meta:
        model = Post
        fields = ['category', 'title', 'contents', 'tags']
        labels = {
            'title': _('Title'),
            'contents': '',
        }


class CommentForm(OneTimeUserFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']
        labels = {
            'contents': '',
        }


class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
