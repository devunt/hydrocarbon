import datetime

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    nick = models.CharField(max_length=16)

    def __str__(self):
        return str(self.user)


class Board(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField()


class Category(models.Model):
    board = models.ForeignKey('Board')
    name = models.CharField(max_length=8)
    slug = models.SlugField()


class Tag(models.Model):
    name = models.CharField(max_length=16)


class Post(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    board = models.ForeignKey('Board')
    category = models.ForeignKey('Category', blank=True, null=True)
    title = models.CharField(max_length=32)
    contents = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    viewcount = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not kwargs.pop('auto_now', False):
            self.modified_time = datetime.datetime.now()
        super(Post, self).save(*args, **kwargs)


def upload_to_func(self, instance, filename):
    checksum = instance.checksum
    return os.path.join(checksum[0], checksum[:1], checksum)

class Attachment(models.Model):
    post = models.ForeignKey('Post')
    name = models.CharField(max_length=64)
    file = models.FileField(upload_to=upload_to_func)
    checksum = models.CharField(max_length=64)
    dlcount = models.PositiveIntegerField(default=0)


class Comment(models.Model):
    post = models.ForeignKey('Post')
    comment = models.ForeignKey('self', related_name='subcomments', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    contents = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)


class Recommendation(models.Model):
    NOT_RECOMMEND = 0
    RECOMMEND = 1
    RECOMMEND_CHOICES = (
        (NOT_RECOMMEND, 'Not recommend'),
        (RECOMMEND, 'Recommend'),
    )
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(protocol='IPv4')
    recommend = models.PositiveSmallIntegerField(choices=RECOMMEND_CHOICES)


class Announcement(models.Model):
    post = models.ForeignKey('Post')
    boards = models.ManyToManyField('Board')
