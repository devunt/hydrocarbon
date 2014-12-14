from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from board.forms import PostCreateForm
from board.mixins import BoardMixin, UserLoggingMixin
from board.models import Board, Post, Vote


class PostCreateView(BoardMixin, UserLoggingMixin, CreateView):
    model = Post
    form_class = PostCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['board'] = self.board
        return kwargs


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.object.board
        return super().get_context_data(**kwargs)


class PostListView(BoardMixin, ListView):
    pagenate_by = 20

    def get_queryset(self):
        return Post.objects.filter(board=self.board).order_by('-created_time')


class RecommendView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        target_type = request.POST.get('type')
        target_id = request.POST.get('target', '')
        recommend = request.POST.get('recommend')

        if ((target_type not in ('p', 'c')) or
            (not target_id.isdigit()) or
            (recommend not in ('++', '-+', '+-', '--'))):
            return JsonResponse({'status': 'badrequest'}, status=400)
        target_id = int(target_id)

        if target_type == 'p':
            try:
                post = Post.objects.get(id=target_id)
            except Post.DoesNotExist:
                return JsonResponse({'status': 'badrequest'}, status=400)
            rqs = Recommendation.objects.filter(post=post)
        else:
            try:
                comment = Comment.objects.get(id=target_id)
            except Comment.DoesNotExist:
                return JsonResponse({'status': 'badrequest'}, status=400)
            rqs = Recommendation.objects.filter(comment=comment)
        if request.user.is_authenticated():
            rqs = rqs.filter(user=request.user)
        else:
            rqs = rqs.filter(ipaddress=request.META['REMOTE_ADDR'])

        if recommend[0] == '+':
            if rqs.exists():
                return JsonResponse({'status': 'alreadyhave'}, status=409)
            r = Recommendation()
            if target_type == 'p':
                r.post = post
            else:
                r.comment = comment
            if recommend[1] == '+':
                r.recommend = Recommendation.UPVOTE
            else:
                r.recommend = Recommendation.DOWNVOTE
            if request.user.is_authenticated():
                r.user = request.user
            r.ipaddress = request.META['REMOTE_ADDR']
            r.save()
            return JsonResponse({'status': 'success'})
        else:
            if recommend[1] == '+':
                rqs = rqs.filter(recommend=Recommendation.UPVOTE)
            else:
                rqs = rqs.filter(recommend=Recommendation.DOWNVOTE)
            if not rqs.exists():
                return JsonResponse({'status': 'notexists'}, status=404)
            r = rqs.first()
            r.delete()
            return JsonResponse({'status': 'success'})
