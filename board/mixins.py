from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from board.forms import PasswordForm
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
        aqs = Announcement.objects.filter(Q(boards=self.board) | Q(boards=None))
        announcement_list = [announcement.post for announcement in aqs]
        kwargs['announcement_list'] = announcement_list
        return super().get_context_data(**kwargs)


class PermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if ((self.object.user is not None) and (self.object.user != request.user)) and \
           (not request.user.is_staff):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def check_permission(self):
        if self.request.user.is_staff:
            return True
        if self.object.user is None:
            password = self.request.POST.get('password')
            if password:
                post_dict = dict(self.request.POST)
                del post_dict['password']
                self.request.POST = post_dict
            if not check_password(password, self.object.onetime_user.password):
                messages.error(self.request, _('Wrong password'))
                return False
        return True

    def _get_context_data(self, **kwargs):
        if not self.request.user.is_staff:
            kwargs['password_form'] = PasswordForm()
        return super().get_context_data(**kwargs)
