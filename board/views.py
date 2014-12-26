from hashlib import md5

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import JsonResponse, QueryDict
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from board.forms import PasswordForm, PostForm
from board.mixins import AjaxMixin, BoardMixin, PostListMixin, PermissionMixin, UserLoggingMixin
from board.models import Attachment, Board, Comment, OneTimeUser, Post, Vote

from hydrocarbon import settings


class IndexView(View):
    def get(self, request, *args, **kwargs):
        board = Board.objects.first()
        return redirect(reverse('board_post_list', kwargs={'board': board.slug}))


class PostCreateView(BoardMixin, UserLoggingMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        qdict = QueryDict('', mutable=True)
        qdict.update({
            'type': 'p',
            'target': str(self.object.id),
            'vote': '++',
        })
        r = self.request
        r.POST = qdict
        v = VoteAjaxView()
        v.post(r)
        return super().get_success_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['authenticated'] = self.request.user.is_authenticated()
        kwargs['board'] = self.board
        return kwargs


class PostUpdateView(PermissionMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        if (not kwargs.pop('authenticated', False)) and self.object.user is None:
            self.get_context_data = self._get_context_data
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get('password'):
            if self.check_permission():
                kwargs['authenticated'] = True
            request.method = 'GET'
            return self.get(request, *args, **kwargs)
        else:
            return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['board'] = self.object.board
        # Anonymous users can't change their OneTimeUser property once they posted
        kwargs['authenticated'] = True
        return kwargs


class PostDeleteView(PermissionMixin, DeleteView):
    model = Post

    def get(self, request, *args, **kwargs):
        if self.object.user is None:
            self.get_context_data = self._get_context_data
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not self.check_permission():
            return self.get(request, *args, **kwargs)
        if self.object.onetime_user is not None:
            self.object.onetime_user.delete()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _('Deleted'))
        return reverse('board_post_list', kwargs={'board': self.object.board.slug})


class PostListView(BoardMixin, PostListMixin, ListView):
    paginate_by = 10
    is_best = False

    def get_queryset(self):
        return Post.objects.filter(board=self.board).order_by('-created_time')

    def get_context_data(self, **kwargs):
        kwargs['is_best'] = self.is_best
        return super().get_context_data(**kwargs)


class PostBestListView(PostListView):
    is_best = True

    def get_queryset(self):
        pqs = super().get_queryset()
        pqs = pqs.annotate(vote=Sum('_votes__vote'))
        pqs = pqs.filter(vote__gte=settings.BOARD_POST_BEST_VOTES)
        return pqs


class PostDetailView(DetailView):
    model = Post

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        self.board = post.board
        post_ids_viewed = self.request.session.get('post_ids_viewed', list())
        if post.id not in post_ids_viewed:
            post.viewcount += 1
            post.save()
            post_ids_viewed.append(post.id)
            self.request.session['post_ids_viewed'] = post_ids_viewed
        return post

    def get_context_data(self, **kwargs):
        if self.request.META.get('HTTP_REFERER') == \
            self.request.build_absolute_uri(
                reverse('board_post_list_best', kwargs={'board': self.board.slug})
            ):
            plv = PostBestListView()
        else:
            plv = PostListView()
        plv.kwargs = dict()
        plv.request = self.request
        plv.dispatch(self.request, board=self.board.slug)
        ctx = plv.get_context_data()
        kwargs.update(ctx)
        kwargs['board'] = self.board
        voted = {'upvoted': False, 'downvoted': False}
        if self.request.user.is_authenticated():
            vqs = self.object._votes.filter(user=self.request.user)
        else:
            vqs = self.object._votes.filter(user=None, ipaddress=self.request.META['REMOTE_ADDR'])
        if vqs.exists():
            vote = vqs.first()
            if vote.vote == Vote.UPVOTE:
                voted['upvoted'] = True
            elif vote.vote == Vote.DOWNVOTE:
                voted['downvoted'] = True
        kwargs['voted'] = voted
        return super().get_context_data(**kwargs)


class VoteAjaxView(AjaxMixin, View):
    def post(self, request):
        target_type = request.POST.get('type')
        target_id = request.POST.get('target', '')
        vote = request.POST.get('vote')
        vote_dicts = request.session.get('vote_dicts', list())

        if ((target_type not in ('p', 'c')) or
            (not target_id.isdigit()) or
            (vote not in ('++', '-+', '+-', '--'))):
            return self.bad_request()
        target_id = int(target_id)

        vote_dict = {'type': target_type, 'id': target_id, 'vote': vote}
        if vote_dict in vote_dicts:
            return JsonResponse({'status': 'alreadyhave'}, status=409)

        if target_type == 'p':
            try:
                post = Post.objects.get(id=target_id)
            except Post.DoesNotExist:
                return self.bad_request()
            vqs = Vote.objects.filter(post=post)
        else:
            try:
                comment = Comment.objects.get(id=target_id)
            except Comment.DoesNotExist:
                return self.bad_request()
            vqs = Vote.objects.filter(comment=comment)
        if request.user.is_authenticated():
            vqs = vqs.filter(user=request.user)
        else:
            vqs = vqs.filter(user=None, ipaddress=request.META['REMOTE_ADDR'])

        if vote[0] == '+':
            if vote[1] == '-' and not request.user.is_authenticated():
                return JsonResponse({'status': 'notauthenticated'}, status=401)
            if vqs.exists():
                return JsonResponse({'status': 'alreadyhave'}, status=409)
            v = Vote()
            if target_type == 'p':
                v.post = post
            else:
                v.comment = comment
            if vote[1] == '+':
                v.vote = Vote.UPVOTE
            else:
                v.vote = Vote.DOWNVOTE
            if request.user.is_authenticated():
                v.user = request.user
            v.ipaddress = request.META['REMOTE_ADDR']
            v.save()
            vote_dicts.append(vote_dict)
            request.session['vote_dicts'] = vote_dicts
            return JsonResponse({'status': 'success', 'current': post.votes if target_type == 'p' else comment.votes})
        else:
            if vote[1] == '+':
                vqs = vqs.filter(vote=Vote.UPVOTE)
            else:
                vqs = vqs.filter(vote=Vote.DOWNVOTE)
            if not vqs.exists():
                return self.not_found()
            v = vqs.first()
            v.delete()
            vote_dict['vote'] = '+' + vote[1]
            if vote_dict in vote_dicts:
                vote_dicts.remove(vote_dict)
                request.session['vote_dicts'] = vote_dicts
            return JsonResponse({'status': 'success', 'current': post.votes if target_type == 'p' else comment.votes})


class FileUploadAjaxView(AjaxMixin, View):
    def post(self, request):
        files = list()
        for f in request.FILES.getlist('files[]'):
            hasher = md5()
            for chunk in f.chunks():
                hasher.update(chunk)
            attachment = Attachment()
            attachment.checksum = hasher.hexdigest()
            attachment.content_type = f.content_type
            attachment.name = f.name
            attachment.file = f
            attachment.save()
            files.append({'name': f.name, 'content_type': f.content_type})
        return JsonResponse({'status': 'success', 'files': files})


class CommentAjaxView(AjaxMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=self.pk)
        except Post.DoesNotExist:
            return self.not_found()
        def _comment_sort_key(comment):
            return comment['votes']['total']
        def _make_list(comments):
            lst = list()
            for comment in comments:
                subcomments = None
                if comment.subcomments.exists():
                    subcomments = _make_list(comment.subcomments.filter(comment=comment))
                voted = {'upvoted': False, 'downvoted': False}
                if request.user.is_authenticated():
                    vqs = comment._votes.filter(user=request.user)
                else:
                    vqs = comment._votes.filter(user=None, ipaddress=request.META['REMOTE_ADDR'])
                if vqs.exists():
                    vote = vqs.first()
                    if vote.vote == Vote.UPVOTE:
                        voted['upvoted'] = True
                    elif vote.vote == Vote.DOWNVOTE:
                        voted['downvoted'] = True
                lst.append({
                    'id': comment.id,
                    'author': comment.author,
                    'iphash': comment.iphash if not comment.user else None,
                    'contents': comment.contents,
                    'created_time': comment.created_time,
                    'votes': comment.votes,
                    'voted': voted,
                    'subcomments': subcomments,
                })
            lst.sort(key=_comment_sort_key, reverse=True)
            return lst
        lst = _make_list(post.comments.filter(comment=None))
        return JsonResponse({'status': 'success', 'comments': {'count': post.comments.count(), 'list': lst}})

    def post(self, request, *args, **kwargs):
        target_type = request.POST.get('type')
        c = Comment()
        if target_type == 'p':
            try:
                c.post = Post.objects.get(pk=self.pk)
            except Post.DoesNotExist:
                return self.not_found()
        elif target_type == 'c':
            try:
                c.comment = Comment.objects.get(pk=self.pk)
                c.post = c.comment.post
            except Comment.DoesNotExist:
                return self.not_found()
        else:
            return self.bad_request()
        if request.user.is_authenticated():
            c.user = request.user
        else:
            ot_user = OneTimeUser()
            ot_user.nick = request.POST.get('ot_nick')
            ot_user.password = make_password(request.POST.get('ot_password'))
            ot_user.save()
            c.onetime_user = ot_user
        c.ipaddress = request.META['REMOTE_ADDR']
        c.contents = request.POST.get('contents')
        c.save()
        qdict = QueryDict('', mutable=True)
        qdict.update({
            'type': 'c',
            'target': str(c.id),
            'vote': '++',
        })
        r = request
        r.POST = qdict
        v = VoteAjaxView()
        v.post(r)
        return self.success()

    def put(self, request, *args, **kwargs):
        try:
            c = Comment.objects.get(pk=self.pk)
        except Comment.DoesNotExist:
            return self.not_found()
        if c.user:
            if (not request.user.is_staff) and (c.user != request.user):
                return self.permission_denied()
        else:
            if (not request.user.is_staff) and not check_password(request.META.get('HTTP_X_HC_PASSWORD'), c.onetime_user.password):
                return self.permission_denied()
        PUT = QueryDict(request.body)
        c.contents = PUT.get('contents')
        c.save()
        return self.success()

    def delete(self, request, *args, **kwargs):
        try:
            c = Comment.objects.get(pk=self.pk)
        except Comment.DoesNotExist:
            return self.not_found()
        if c.user:
            if (not request.user.is_staff) and (c.user != request.user):
                return self.permission_denied()
        else:
            if (not request.user.is_staff) and not check_password(request.META.get('HTTP_X_HC_PASSWORD'), c.onetime_user.password):
                return self.permission_denied()
            c.onetime_user.delete()
        c.delete()
        return self.success()
