from django.http import Http404
from django.shortcuts import render

from board.models import Board


class BoardMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.board = Board.objects.get(slug=kwargs['board'])
        except Board.DoesNotExist:
            return render(request, 'errors/board_404.html', status=404)
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.board = self.board
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)


class UserLoggingMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user if self.request.user.is_authenticated() else None
        form.instance.ipaddress = self.request.META['REMOTE_ADDR']
        return super().form_valid(form)
