from hashlib import sha224

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import aggregates
from django.db.models.sql import aggregates as sql_aggregates
from django.utils import timezone
from custom_user.models import AbstractEmailUser
from froala_editor.fields import FroalaField
from jsonfield import JSONField

from board.utils import clean_html, get_upload_path, normalize


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

    @property
    def unread_notifications(self):
        return self._notifications.filter(checked_time=None)

    @property
    def recent_notifications(self):
        return self.all_notifications[:10]

    @property
    def all_notifications(self):
        return self._notifications.all()

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
    TYPE_ANNOUNCEMENT = 1
    TYPE_LIST = 2
    TYPE_CHOICES = (
        (TYPE_ANNOUNCEMENT, 'Announcement board'),
        (TYPE_LIST, 'List type'),
    )
    name = models.CharField(max_length=16)
    slug = models.SlugField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_LIST)

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
    title = models.CharField(max_length=50)
    contents = FroalaField()
    tags = models.ManyToManyField('Tag', blank=True, null=True, related_name='posts')
    viewcount = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        self.contents = clean_html(self.contents)
        if kwargs.pop('auto_now', True):
            self.modified_time = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']


class Comment(AuthorModelMixin, VotableModelMixin, models.Model):
    post = models.ForeignKey('Post', related_name='comments')
    comment = models.ForeignKey('self', related_name='subcomments', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments', on_delete=models.SET_NULL)
    onetime_user = models.OneToOneField('OneTimeUser', blank=True, null=True, related_name='comment', on_delete=models.SET_NULL)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    contents = FroalaField(options=settings.FROALA_EDITOR_OPTIONS_COMMENT)
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def depth(self):
        def _depth(c, d=0):
            if c.comment is not None:
                return _depth(c.comment, d + 1)
            return d
        return _depth(self)

    def save(self, *args, **kwargs):
        self.contents = clean_html(self.contents)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return (reverse('post_detail', kwargs={'pk': self.post.id}) + '#c{0}'.format(self.id))

    class Meta:
        ordering = ['-created_time']


class Vote(models.Model):
    DOWNVOTE = -1
    UPVOTE = 1
    VOTE_CHOICES = (
        (DOWNVOTE, 'Not recommend'),
        (UPVOTE, 'Recommend'),
    )
    post = models.ForeignKey('Post', blank=True, null=True, related_name='_votes')
    comment = models.ForeignKey('Comment', blank=True, null=True, related_name='_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='_votes', on_delete=models.SET_NULL)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)


class Announcement(models.Model):
    post = models.OneToOneField('Post', related_name='announcement')
    boards = models.ManyToManyField('Board', blank=True, null=True, related_name='announcements')


class ImageAttachment(models.Model):
    name = models.CharField(max_length=250)
    file = models.ImageField(max_length=256, upload_to=get_upload_path)
    checksum = models.CharField(max_length=32, unique=True)


class FileAttachment(models.Model):
    name = models.CharField(max_length=250)
    file = models.FileField(max_length=256, upload_to=get_upload_path)
    checksum = models.CharField(max_length=32, unique=True)


class Notification(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='sent_notifications')
    from_onetime_user = models.OneToOneField('OneTimeUser', blank=True, null=True, related_name='sent_notification')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='_notifications')
    data = JSONField()
    created_time = models.DateTimeField(auto_now_add=True)
    checked_time = models.DateTimeField(blank=True, null=True)

    @classmethod
    def create(cls, from_user, to_user, data, **kwargs):
        notification = cls(**kwargs)
        if isinstance(from_user, get_user_model()):
            notification.from_user = from_user
        elif isinstance(from_user, OneTimeUser):
            notification.from_onetime_user = from_user
        notification.to_user = to_user
        notification.data = data
        notification.save()
        return notification

    @staticmethod
    def set_as_checked(user):
        user.unread_notifications.update(checked_time=timezone.now())

    class Meta:
        ordering = ['-created_time']


class Block(models.Model):
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blocks_executed')
    ipaddress = models.GenericIPAddressField(protocol='IPv4', unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()
    reason = models.CharField(max_length=256)

    @staticmethod
    def is_blocked(ipaddress):
        try:
            block = Block.objects.get(ipaddress=ipaddress)
            if block.expiration_time <= timezone.now():
                block.delete()
                raise Block.DoesNotExist
        except Block.DoesNotExist:
            return False
        else:
            return block
