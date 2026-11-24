from functools import wraps

from django.core.exceptions import ImproperlyConfigured

from .templatetags import meta

try:
    from jinja2 import Markup
except ImportError:
    Markup = None


class MetaProxy(object):

    def __init__(self, *args, **kwargs):
        if Markup is None:
            raise ImproperlyConfigured('Jinja2 package is not installed')

    def __getattr__(self, item):
        f = getattr(meta, item)

        @wraps(f)
        def wrapped(*args, **kwargs):
            tag = f(*args, **kwargs)
            return Markup(tag)

        return wrapped
