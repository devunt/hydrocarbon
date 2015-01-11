import bleach
import os
import re

from collections import defaultdict
from hashlib import md5
from urllib.parse import quote_plus, urlparse

from django.conf import settings
from django.http import QueryDict
from django.utils.encoding import iri_to_uri


RE_EMPTYHTML = re.compile(r'<p>\s*(?:(?:&nbsp;|<br\s*/?>)\s*)*</p>')

FIRSTS = ('ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')
MIDDLES = ('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅗㅏ', 'ㅗㅐ', 'ㅗㅣ', 'ㅛ', 'ㅜ', 'ㅜㅓ', 'ㅜㅔ', 'ㅜㅣ', 'ㅠ', 'ㅡ', 'ㅡㅣ', 'ㅣ')
LASTS = ('', 'ㄱ', 'ㄲ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅎ', 'ㄷ', 'ㄹ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅍ', 'ㄹㅎ', 'ㅁ', 'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

def _normalize(c):
    if '가' <= c <= '힣':
        offset = ord(c) - ord('가')
        first = FIRSTS[offset // (len(MIDDLES) * len(LASTS))]
        middle = MIDDLES[(offset // len(LASTS)) % len(MIDDLES)]
        last = LASTS[offset % len(LASTS)]
        return '{0} {1} {2}'.format(first, middle, last)
    return c

def normalize(s):
    return ' '.join(map(_normalize, s))


def clean_html(html):
    return bleach.clean(html,
        tags=settings.BLEACH_ALLOWED_TAGS,
        attributes=settings.BLEACH_ALLOWED_ATTRIBUTES,
        styles=settings.BLEACH_ALLOWED_STYLES
    )


def is_empty_html(html):
    cleaned = clean_html(html)
    replaced = re.sub(RE_EMPTYHTML, '', cleaned)
    return (replaced.strip() == '')


def get_upload_path(instance, filename):
    checksum = instance.checksum
    return os.path.join(checksum[0], checksum[:2], filename)


def treedict():
    return defaultdict(treedict)


# From https://bitbucket.org/monwara/django-url-tools/raw/9ce1dbd9b3609b9cebd8445ce787dff640ffedbc/url_tools/helper.py
class UrlHelper(object):
    def __init__(self, full_path):
        # If full_path is an UrlHelper instance, extract the full path from it
        if type(full_path) is UrlHelper:
            full_path = full_path.get_full_path()

        # parse the path
        r = urlparse(full_path)
        self.path = r.path
        self.fragment = r.fragment
        self.query_dict = QueryDict(r.query, mutable=True)

    def get_query_string(self, **kwargs):
        return self.query_dict.urlencode(**kwargs)

    def get_query_data(self):
        return self.query_dict

    def update_query_data(self, **kwargs):
        for key, val in kwargs.items():
            if not isinstance(val, str) and hasattr(val, '__iter__'):
                self.query_dict.setlist(key, val)
            else:
                self.query_dict[key] = val

    def get_path(self):
        return self.path

    def get_full_path(self, **kwargs):
        query_string = self.get_query_string(**kwargs)
        if query_string:
            query_string = '?%s' % query_string
        fragment = self.fragment and '#%s' % iri_to_uri(self.fragment) or ''

        return '%s%s%s' % (
            iri_to_uri(self.get_path()),
            query_string,
            fragment
        )

    def get_full_quoted_path(self, **kwargs):
        return quote_plus(self.get_full_path(**kwargs), safe='/')

    def overload_params(self, **kwargs):
        for key, val in kwargs.items():
            uniques = set(self.query_dict.getlist(key))
            uniques.add(val)
            self.query_dict.setlist(key, list(uniques))

    def del_param(self, param):
        try:
            del self.query_dict[param]
        except KeyError:
            pass  # Fail silently

    def del_params(self, *params, **kwargs):
        if not params and not kwargs:
            self.query = {}
            return
        if params:
            for param in params:
                self.del_param(param)
        if kwargs:
            for key, val in kwargs.items():
                to_keep = [x for x in self.query_dict.getlist(key)
                           if not x.startswith(val)]
                self.query_dict.setlist(key, to_keep)

    def toggle_params(self, **params):
        for param, value in params.items():
            value = str(value)
            if value in self.query_dict.getlist(param):
                self.del_params(**{param: value})
            else:
                self.overload_params(**{param: value})

    @property
    def hash(self):
        _md5 = md5()
        _md5.update(self.get_full_path())
        return _md5.hexdigest()

    @property
    def query(self):
        return self.get_query_data()

    @query.setter
    def query(self, value):
        if type(value) is dict:
            self.query_dict = QueryDict('', mutable=True)
            self.update_query_data(**value)
        else:
            self.query_dict = QueryDict(value, mutable=True)

    @property
    def query_string(self):
        return self.get_query_string()

    @query_string.setter
    def query_string(self, value):
        self.query_dict = QueryDict(value, mutable=True)

    def __str__(self):
        return self.get_full_path()
