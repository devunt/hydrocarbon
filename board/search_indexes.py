from django.conf import settings
from haystack import indexes
from importlib import import_module

from board.models import Comment, Post, Tag


module, cls = settings.SEARCH_INDEX_CLASS.rsplit('.', maxsplit=1)
module = import_module(module)
SEARCH_INDEX_CLASS = getattr(module, cls)


class PostIndex(SEARCH_INDEX_CLASS, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    board = indexes.CharField(model_attr='board__slug')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Post


class CommentIndex(SEARCH_INDEX_CLASS, indexes.Indexable):
    text = indexes.CharField(model_attr='contents', document=True)
    post = indexes.IntegerField(model_attr='post__id', indexed=False)
    board = indexes.CharField(model_attr='post__board__slug')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Comment


class TagIndex(SEARCH_INDEX_CLASS, indexes.Indexable):
    text = indexes.CharField(model_attr='normalized', document=True)

    def get_model(self):
        return Tag
