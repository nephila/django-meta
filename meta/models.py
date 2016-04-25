# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import contextlib
from copy import copy

from django.conf import settings as dj_settings

from . import settings

NEED_REQUEST_OBJECT_ERR_MSG = """
Meta models needs request objects when initializing if sites framework is not used.
""".strip()


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
        'fb_pages': settings.FB_PAGES,
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
        'custom_namespace': settings.OG_NAMESPACES,
    }

    def get_meta(self, request=None):
        """
        Retrieve the meta data configuration
        """
        metadata = copy(self._metadata_default)
        metadata.update(self._metadata)
        return metadata

    def _retrieve_data(self, request, metadata):
        """
        Build the data according to the metadata configuration
        """
        with self._set_request(request):
            for field, value in metadata.items():
                if value:
                    data = self._get_meta_value(field, value)
                    yield field, data

    def _get_meta_value(self, field, value):
        """
        Build the data according to a

        :param field: metadata field name
        :param value: provided value
        :return: data
        """
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
            return data

    def as_meta(self, request=None):
        """
        Method that generates the Meta object (from django-meta)
        """
        from meta.views import Meta
        metadata = self.get_meta(request)
        meta = Meta()
        for field, data in self._retrieve_data(request, metadata):
            setattr(meta, field, data)
        for field in ('og_description', 'twitter_description', 'gplus_description'):
            generaldesc = getattr(meta, 'description', False)
            if not getattr(meta, field, False) and generaldesc:
                setattr(meta, field, generaldesc)
        return meta

    @contextlib.contextmanager
    def _set_request(self, request):
        """
        Context processor that sets the requst on the current instance
        """
        self._request = request
        yield
        delattr(self, '_request')

    def get_request(self):
        """
        Retrieve request from current instance
        """
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
        """
        Sample method to return the author facebook URL
        """
        try:
            return self.get_author().fb_url
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_name(self):
        """
        Sample method to return the author full name
        """
        try:
            return self.get_author().get_full_name()
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_twitter(self):
        """
        Sample method to return the author twitter account
        """
        try:
            return self.get_author().twitter_profile
        except AttributeError:  # pragma: no cover
            return ''

    def get_author_gplus(self):
        """
        Sample method to return the author google plus URL
        """
        try:
            return self.get_author().gplus_profile
        except AttributeError:  # pragma: no cover
            return ''

    def get_meta_protocol(self):
        """
        Current http protocol
        """
        return dj_settings.META_SITE_PROTOCOL

    def build_absolute_uri(self, url):
        """
        Return the full url for the provided url argument
        """
        request = self.get_request()
        if request:
            return request.build_absolute_uri(url)

        if not dj_settings.META_USE_SITES:
            raise RuntimeError(NEED_REQUEST_OBJECT_ERR_MSG)

        from django.contrib.sites.models import Site
        s = Site.objects.get_current()
        meta_protocol = self.get_meta_protocol()
        if url.startswith('http'):
            return url
        if s.domain.find('http') > -1:
            return '{0}{1}'.format(s.domain, url)  # pragma: no cover
        else:
            if url.startswith('/'):
                return '{0}://{1}{2}'.format(meta_protocol, s.domain, url)
            else:
                return '{0}://{1}/{2}'.format(meta_protocol, s.domain, url)
