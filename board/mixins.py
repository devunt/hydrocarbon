from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from board.forms import PasswordForm
from board.models import DefaultSum
from board.models import Announcement, Board, Post, OneTimeUser, User


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
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        o = request.GET.get('o')
        if o is None:
            o = '+ct'
        d = {'mt': 'modified_time', 'vt': 'vote', 'vc': 'viewcount'}
        order_by = ('-' if o[0] == '+' else '') + d.get(o[1:], 'created_time')
        request.session['post_list_order_by'] = order_by
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if hasattr(self, 'get_base_queryset'):
            pqs = self.get_base_queryset()
        else:
            pqs = super().get_queryset()
        order_by = self.request.session.get('post_list_order_by')
        pqs = pqs.annotate(vote=DefaultSum('_votes__vote', default=0))
        pqs = pqs.order_by(order_by, '-created_time')
        if hasattr(self, 'queryset_post_filter'):
            pqs = self.queryset_post_filter(pqs)
        return pqs

    def get_context_data(self, **kwargs):
        order_by = self.request.session.get('post_list_order_by')
        odict = dict()
        if order_by.startswith('-'):
            odict['order'] = 'asc'
            odict['column'] = order_by[1:]
        else:
            odict['order'] = 'desc'
            odict['column'] = order_by
        kwargs['order_by'] = odict
        kwargs['BOARD_POST_BLIND_VOTES'] = settings.BOARD_POST_BLIND_VOTES
        return super().get_context_data(**kwargs)


class BPostListMixin(PostListMixin):
    template_name = 'board/postlist/with_board.html'

    def get_base_queryset(self):
        pqs = Post.objects.filter(board=self.board, announcement=None)
        return pqs

    def get_context_data(self, **kwargs):
        aqs = Announcement.objects.filter(Q(boards=self.board) | Q(boards=None))
        announcement_list = [announcement.post for announcement in aqs]
        kwargs['announcement_list'] = announcement_list
        return super().get_context_data(**kwargs)
