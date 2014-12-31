from haystack import indexes

from board.models import Post, Tag


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    board = indexes.CharField(model_attr='board__slug')
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Post


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(model_attr='normalized', document=True)

    def get_model(self):
        return Tag
