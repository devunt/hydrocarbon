from hashlib import md5

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from board.forms import PostForm
from board.mixins import BoardMixin, UserLoggingMixin
from board.models import Attachment, Board, Post, Vote


class IndexView(View):
    def get(self, request, *args, **kwargs):
        board = Board.objects.first()
        return redirect(reverse('board_post_list', kwargs={'board': board.slug}))


class PostCreateView(BoardMixin, UserLoggingMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        v = Vote()
        v.user = self.object.user
        v.ipaddress = self.object.ipaddress
        v.post = self.object
        v.vote = Vote.UPVOTE
        v.save()
        return super().get_success_url()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['authenticated'] = self.request.user.is_authenticated()
        kwargs['board'] = self.board
        return kwargs


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['board'] = self.object.board
        # Anonymous users can't change their OneTimeUser property once they posted
        kwargs['authenticated'] = True
        return kwargs


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post_ids_viewed = self.request.session.get('post_ids_viewed', list())
        if post.id not in post_ids_viewed:
            post.viewcount += 1
            post.save()
            post_ids_viewed.append(post.id)
            self.request.session['post_ids_viewed'] = post_ids_viewed
        return post

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.object.board
        kwargs['post_list'] = self.object.board.posts.order_by('-created_time')
        voted = {'upvoted': False, 'downvoted': False}
        if self.request.user.is_authenticated():
            vqs = self.object._votes.filter(user=self.request.user)
        else:
            vqs = self.object._votes.filter(ipaddress=self.request.META['REMOTE_ADDR'])
        if vqs.exists():
            vote = vqs.first()
            if vote.vote == Vote.UPVOTE:
                voted['upvoted'] = True
            elif vote.vote == Vote.DOWNVOTE:
                voted['downvoted'] = True
        kwargs['voted'] = voted
        return super().get_context_data(**kwargs)


class PostListView(BoardMixin, ListView):
    pagenate_by = 20

    def get_queryset(self):
        return Post.objects.filter(board=self.board).order_by('-created_time')


class VoteAjaxView(View):
    def post(self, request):
        target_type = request.POST.get('type')
        target_id = request.POST.get('target', '')
        vote = request.POST.get('vote')

        if ((target_type not in ('p', 'c')) or
            (not target_id.isdigit()) or
            (vote not in ('++', '-+', '+-', '--'))):
            return JsonResponse({'status': 'badrequest'}, status=400)
        target_id = int(target_id)

        if target_type == 'p':
            try:
                post = Post.objects.get(id=target_id)
            except Post.DoesNotExist:
                return JsonResponse({'status': 'badrequest'}, status=400)
            rqs = Vote.objects.filter(post=post)
        else:
            try:
                comment = Comment.objects.get(id=target_id)
            except Comment.DoesNotExist:
                return JsonResponse({'status': 'badrequest'}, status=400)
            rqs = Vote.objects.filter(comment=comment)
        if request.user.is_authenticated():
            rqs = rqs.filter(user=request.user)
        else:
            rqs = rqs.filter(ipaddress=request.META['REMOTE_ADDR'])

        if vote[0] == '+':
            if vote[1] == '-' and not request.user.is_authenticated():
                return JsonResponse({'status': 'notauthenticated'}, status=401)
            if rqs.exists():
                return JsonResponse({'status': 'alreadyhave'}, status=409)
            r = Vote()
            if target_type == 'p':
                r.post = post
            else:
                r.comment = comment
            if vote[1] == '+':
                r.vote = Vote.UPVOTE
            else:
                r.vote = Vote.DOWNVOTE
            if request.user.is_authenticated():
                r.user = request.user
            r.ipaddress = request.META['REMOTE_ADDR']
            r.save()
            return JsonResponse({'status': 'success', 'current': post.votes if target_type == 'p' else comment.votes})
        else:
            if vote[1] == '+':
                rqs = rqs.filter(vote=Vote.UPVOTE)
            else:
                rqs = rqs.filter(vote=Vote.DOWNVOTE)
            if not rqs.exists():
                return JsonResponse({'status': 'notexists'}, status=404)
            r = rqs.first()
            r.delete()
            return JsonResponse({'status': 'success', 'current': post.votes if target_type == 'p' else comment.votes})


class FileUploadAjaxView(View):
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
