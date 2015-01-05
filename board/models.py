import bleach

from hashlib import sha224

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import aggregates
from django.db.models.sql import aggregates as sql_aggregates
from django.utils import timezone
from custom_user.models import AbstractEmailUser
from redactor.fields import RedactorField

from board.utils import normalize


class DefaultSum(aggregates.Aggregate):
    name = 'DefaultSum'

class SQLDefaultSum(sql_aggregates.Sum):
    sql_template = 'COALESCE(%(function)s(%(field)s), %(default)s)'

setattr(sql_aggregates, 'DefaultSum', SQLDefaultSum)


class User(AbstractEmailUser):
    nickname = models.CharField(max_length=16, unique=True,
        validators=[MinLengthValidator(2)])

    @property
    def total_score(self):
        post_votes = self.posts.aggregate(score=DefaultSum('_votes__vote', default=0))
        comment_votes = self.comments.aggregate(score=DefaultSum('_votes__vote', default=0))
        return post_votes['score'] + comment_votes['score']

    @property
    def score(self):
        votes = {
            'posts': {
                'upvotes': Vote.objects.filter(post__in=self.posts.all(), vote=Vote.UPVOTE).count(),
                'downvotes': Vote.objects.filter(post__in=self.posts.all(), vote=Vote.DOWNVOTE).count(),
            },
            'comments': {
                'upvotes': Vote.objects.filter(comment__in=self.comments.all(), vote=Vote.UPVOTE).count(),
                'downvotes': Vote.objects.filter(comment__in=self.comments.all(), vote=Vote.DOWNVOTE).count(),
            },
        }
        return votes

    def __str__(self):
        return self.nickname

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user': self.id})


class OneTimeUser(models.Model):
    nick = models.CharField(max_length=16)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.nick


class Board(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_post_list', kwargs={'board': self.slug})


class Category(models.Model):
    board = models.ForeignKey('Board', related_name='categories')
    name = models.CharField(max_length=8)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    @property
    def normalized(self):
        return normalize(self.name)

    def __str__(self):
        return self.name


class VotableModelMixin:
    @property
    def votes(self):
        vd = dict()
        vd['upvote'] = self._votes.filter(vote=Vote.UPVOTE).count()
        vd['downvote'] = self._votes.filter(vote=Vote.DOWNVOTE).count()
        vd['total'] = vd['upvote'] - vd['downvote']
        return vd


class AuthorModelMixin:
    @property
    def author(self):
        if self.user:
            return self.user.nickname
        else:
            return self.onetime_user.nick

    @property
    def iphash(self):
        return sha224(self.ipaddress.encode()).hexdigest()[:10]


class Post(AuthorModelMixin, VotableModelMixin, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='posts', on_delete=models.SET_NULL)
    onetime_user = models.OneToOneField('OneTimeUser', blank=True, null=True, related_name='post', on_delete=models.SET_NULL)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    board = models.ForeignKey('Board', related_name='posts')
    category = models.ForeignKey('Category', blank=True, null=True, related_name='posts')
    title = models.CharField(max_length=32)
    contents = RedactorField()
    tags = models.ManyToManyField('Tag', blank=True, null=True, related_name='posts')
    viewcount = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        self.contents = bleach.clean(self.contents,
            tags=settings.BLEACH_ALLOWED_TAGS,
            attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
            styles=settings.BLEACH_ALLOWED_STYLES
        )
        if kwargs.pop('auto_now', True):
            self.modified_time = timezone.now()
        super().save(*args, **kwargs)


class Comment(AuthorModelMixin, VotableModelMixin, models.Model):
    post = models.ForeignKey('Post', related_name='comments')
    comment = models.ForeignKey('self', related_name='subcomments', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments', on_delete=models.SET_NULL)
    onetime_user = models.OneToOneField('OneTimeUser', blank=True, null=True, related_name='comment', on_delete=models.SET_NULL)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    contents = RedactorField()
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.contents = bleach.clean(self.contents,
            tags=settings.BLEACH_ALLOWED_TAGS,
            attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
            styles=settings.BLEACH_ALLOWED_STYLES
        )
        super().save(*args, **kwargs)


class Vote(models.Model):
    DOWNVOTE = -1
    UPVOTE = 1
    VOTE_CHOICES = (
        (DOWNVOTE, 'Not recommend'),
        (UPVOTE, 'Recommend'),
    )
    post = models.ForeignKey('Post', blank=True, null=True, related_name='_votes')
    comment = models.ForeignKey('Comment', blank=True, null=True, related_name='_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='_votes')
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)


class Announcement(models.Model):
    post = models.OneToOneField('Post', related_name='announcement')
    boards = models.ManyToManyField('Board', blank=True, null=True, related_name='announcements')
