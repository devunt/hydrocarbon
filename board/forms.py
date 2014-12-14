from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteInplaceWidget
from registration.forms import RegistrationFormUniqueEmail

from board.models import Board, Category, Post


class HCRegistrationForm(RegistrationFormUniqueEmail):
    nick = forms.CharField(label=_('Nickname:'), min_length=2, max_length=16)


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        board = kwargs.pop('board')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(board=board)

    class Meta:
        model = Post
        fields = ['category', 'title', 'contents', 'tags']
        widgets = {
            'contents': SummernoteInplaceWidget(),
            'tags': TextInput(),
        }
        labels = {
            'contents': '',
        }
