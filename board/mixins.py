from django.contrib.auth.hashers import make_password
from django.http import Http404, JsonResponse
from django.shortcuts import render

from board.models import Announcement, Board, OneTimeUser


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
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
        else:
            ot_user = OneTimeUser()
            ot_user.nick = form.cleaned_data['onetime_nick']
            ot_user.password = make_password(form.cleaned_data['onetime_password'])
            ot_user.save()
            form.instance.onetime_user = ot_user
        form.instance.ipaddress = self.request.META['REMOTE_ADDR']
        return super().form_valid(form)


class AjaxMixin:
    def bad_request(self):
        return JsonResponse({'status': 'badrequest'}, status=400)

    def permission_denied(self):
        return JsonResponse({'status': 'permissiondenied'}, status=403)

    def not_found(self):
        return JsonResponse({'status': 'notexists'}, status=404)

    def success(self):
        return JsonResponse({'status': 'success'})


class PostListMixin:
    def get_context_data(self, **kwargs):
        announcement_list = list()
        for announcement in self.board.announcements.all():
            post = announcement.post
            post.is_announcement = True
            announcement_list.append(post)
        kwargs['announcement_list'] = announcement_list
        return super().get_context_data(**kwargs)
