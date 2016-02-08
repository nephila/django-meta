# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import contextlib
import warnings
from copy import copy

from django.conf import settings as dj_settings
from django.contrib.sites.models import Site

from . import settings


class ModelMeta(object):
    """
    Meta information mixin.
    """
    _metadata = {}
    _metadata_default = {
        'title': False,
        'description': False,
        'og_description': False,
        'twitter_description': False,
        'gplus_description': False,
        'keywords': False,
        'image': settings.DEFAULT_IMAGE,
        'object_type': settings.DEFAULT_TYPE,
        'og_type': settings.FB_TYPE,
        'og_app_id': settings.FB_APPID,
        'og_profile_id': settings.FB_PROFILE_ID,
        'og_publisher': settings.FB_PUBLISHER,
        'og_author_url': settings.FB_AUTHOR_URL,
        'twitter_type': settings.TWITTER_TYPE,
        'twitter_site': settings.TWITTER_SITE,
        'twitter_author': settings.TWITTER_AUTHOR,
        'gplus_type': settings.GPLUS_TYPE,
        'gplus_author': settings.GPLUS_AUTHOR,
        'published_time': False,
        'modified_time': False,
        'expiration_time': False,
        'tag': False,
        'url': False,
        'locale': False,
    }

    def get_meta(self, request=None):
        metadata = copy(self._metadata_default)
        metadata.update(self._metadata)
        return metadata

    def as_meta(self, request=None):
        """
        Method that generates the Meta object (from django-meta)
        """
        from meta.views import Meta
        metadata = self.get_meta(request)
        meta = Meta()
        with self._set_request(request):
            for field, value in metadata.items():
                if value:
                    attr = getattr(self, value, False)
                    if attr is not False:
                        if callable(attr):
                            try:
                                data = attr(field)
                            except TypeError:
                                data = attr()
                        else:
                            data = attr
                    else:
                        data = value
                    setattr(meta, field, data)
        for field in ('og_description', 'twitter_description', 'gplus_description'):
            generaldesc = getattr(meta, 'description', False)
            if not getattr(meta, field, False) and generaldesc:
                setattr(meta, field, generaldesc)
        return meta

    @contextlib.contextmanager
    def _set_request(self, request):
        self._request = request
        yield
        delattr(self, '_request')

    def get_request(self):
        return getattr(self, '_request', None)

    def get_author(self):
        """
        Retrieve the author object. This is meant to be overridden in the model
        to return the actual author instance (e.g.: the user object).
        """
        class Author(object):
            fb_url = None
            twitter_profile = None
            gplus_profile = None

            def get_full_name(self):  # pragma: no cover
                return None
        return Author()

    def get_author_url(self):
        try:
            return self.get_author().fb_url
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_name(self):
        try:
            return self.get_author().get_full_name()
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_twitter(self):
        try:
            return self.get_author().twitter_profile
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_gplus(self):
        try:
            return self.get_author().gplus_profile
        except AttributeError:  # pragma: no cover
            return ''

    def get_meta_protocol(self):
        return dj_settings.META_SITE_PROTOCOL

    def make_full_url(self, url):
        warnings.warn(
            'make_full_url is deprecated and it will be removed in 0.3',
            DeprecationWarning
        )
        return self.build_absolute_uri(url)

    def build_absolute_uri(self, url):
        request = self.get_request()
        if request:
            return request.build_absolute_uri(url)
        s = Site.objects.get_current()
        meta_protocol = self.get_meta_protocol()
        if url.startswith('http'):
            return url
        if s.domain.find('http') > -1:
            return "%s%s" % (s.domain, url)  # pragma: no cover
        else:
            if url.startswith('/'):
                return "%s://%s%s" % (meta_protocol, s.domain, url)
            else:
                return "%s://%s/%s" % (meta_protocol, s.domain, url)
