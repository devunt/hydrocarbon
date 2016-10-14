from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from board.forms import PasswordForm
from board.models import Announcement, Board, Post, OneTimeUser, User
from board.pagination import HCPaginator


class BoardURLMixin:
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


class UserURLMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = User.objects.get(pk=kwargs['user'])
        except User.DoesNotExist:
            return render(request, 'errors/user_404.html', status=404)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['u'] = self.user
        return super().get_context_data(**kwargs)


class AjaxMixin:
    def bad_request(self):
        return JsonResponse({'status': 'badrequest'}, status=400)

    def permission_denied(self):
        return JsonResponse({'status': 'permissiondenied'}, status=403)

    def not_found(self):
        return JsonResponse({'status': 'notexists'}, status=404)

    def success(self):
        return JsonResponse({'status': 'success'})


class UserFormMixin:
    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
        else:
            ot_user = OneTimeUser()
            nick = form.cleaned_data['onetime_nick']
            password = form.cleaned_data['onetime_password']
            self.request.session['onetime_user'] = {'nick': nick, 'password': password}
            ot_user.nick = nick
            ot_user.password = make_password(password)
            ot_user.save()
            form.instance.onetime_user = ot_user
        form.instance.ipaddress = self.request.META['REMOTE_ADDR']
        return super().form_valid(form)


class PermissionCheckMixin:
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

    def show_password_form(self):
        self.get_context_data = self.get_context_data_with_password

    def get_context_data_with_password(self, **kwargs):
        if not self.request.user.is_staff:
            kwargs['password_form'] = PasswordForm()
        return super().get_context_data(**kwargs)


class PostListMixin:
    template_name = 'board/postlist/base.html'
    paginate_by = 20
    paginator_class = HCPaginator
    order_by = 'created_time'
    annotate_votes = False

    def get(self, request, *args, **kwargs):
        o = request.GET.get('o')
        if o is None:
            o = '+ct'
        d = {'mt': 'modified_time', 'vt': 'vote', 'vc': 'viewcount'}
        self.order_by = ('-' if o[0] == '+' else '') + d.get(o[1:], 'created_time')
        if 'vote' in self.order_by:
            self.annotate_votes = True
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if hasattr(self, 'get_base_queryset'):
            pqs = self.get_base_queryset()
        else:
            pqs = super().get_queryset()
        if self.annotate_votes:
            pqs = pqs.annotate(vote=Coalesce(models.Sum('_votes__vote'), 0))
        pqs = pqs.order_by(self.order_by, '-created_time')
        if hasattr(self, 'queryset_post_filter'):
            pqs = self.queryset_post_filter(pqs)
        return pqs

    def get_context_data(self, **kwargs):
        odict = dict()
        if self.order_by.startswith('-'):
            odict['order'] = 'asc'
            odict['column'] = self.order_by[1:]
        else:
            odict['order'] = 'desc'
            odict['column'] = self.order_by
        kwargs['order_by'] = odict
        kwargs['BOARD_POST_BLIND_VOTES'] = settings.BOARD_POST_BLIND_VOTES
        return super().get_context_data(**kwargs)


class BPostListMixin(PostListMixin):
    template_name = 'board/postlist/with_board.html'

    def get_base_queryset(self):
        if self.board.type == Board.TYPE_ANNOUNCEMENT:
            pqs = Post.objects.filter(board=self.board)
        else:
            pqs = Post.objects.filter(board=self.board, announcement=None)
        return pqs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if (kwargs['page_obj'].number == 1) and (self.board.type != Board.TYPE_ANNOUNCEMENT):
            aqs = Announcement.objects.filter(Q(boards=self.board) | Q(boards=None))
            aqs = aqs.order_by('-post__created_time')
            announcement_list = [announcement.post for announcement in aqs]
            kwargs['announcement_list'] = announcement_list
        return kwargs
