from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from board.forms import PostCreateForm
from board.mixins import BoardMixin, UserLoggingMixin
from board.models import Board, Post


class PostCreateView(BoardMixin, UserLoggingMixin, CreateView):
    model = Post
    form_class = PostCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['slug'] = self.kwargs['board']
        return kwargs


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.object.board
        return super().get_context_data(**kwargs)


class PostListView(BoardMixin, ListView):
    model = Post
    pass
