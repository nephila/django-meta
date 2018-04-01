# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import contextlib
from copy import copy

from django.conf import settings as dj_settings
from django.db.models import Manager
from django.utils.functional import cached_property

from . import settings
from .views import FullUrlMixin

NEED_REQUEST_OBJECT_ERR_MSG = """
Meta models needs request objects when initializing if sites framework is not used.
""".strip()


class ModelMeta(FullUrlMixin):
    """
    Meta information mixin.
    """
    _metadata = {}
    """
    Metadata configuration dictionary

    `_metadata` dict values can be:

        * name of object method taking the field name as parameter
        * name of object method taking no parameters
        * name of object attribute
        * name of callable taking the field name as parameter
        * name of callable taking no parameters
        * literal value

    They are checked in the given order: the first that matches is returned.

    Callable must be available in the module (i.e.: imported if not defined in the module itself)
    """
    _metadata_default = {
        'title': False,
        'og_title': False,
        'twitter_title': False,
        'gplus_title': False,
        'description': False,
        'og_description': False,
        'twitter_description': False,
        'gplus_description': False,
        'keywords': False,
        'image': settings.DEFAULT_IMAGE,
        'image_width': False,
        'image_height': False,
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
        'gplus_publisher': settings.GPLUS_PUBLISHER,
        'published_time': False,
        'modified_time': False,
        'expiration_time': False,
        'tag': False,
        'url': False,
        'locale': False,
        'custom_namespace': settings.OG_NAMESPACES,
    }
    _schema = {}
    """
    schema.org properties dictionary

    `_metadata` dict values can be:

        * name of object method taking the field name as parameter
        * name of object method taking no parameters
        * name of object attribute
        * name of callable taking the field name as parameter
        * name of callable taking no parameters
        * literal value

    They are checked in the given order: the first that matches is returned.

    Callable must be available in the module (i.e.: imported if not defined in the module itself)

    If the resulting value is a :py:class:`~meta.models.ModelMeta` or :py:class:`~meta.views.Meta` instance
    its schema is set in the schema.org dataset.

    See :ref:`a sample implementation <schema.model>`.
    """

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
        Build metadata values from :py:attr:`_metadata`

        :param field: metadata field name
        :param value: provided value
        :return: data
        """

        def process_value(item):
            if isinstance(item, Manager):
                return list(item.all())
            elif callable(item):
                try:
                    return item(field)
                except TypeError:
                    return item()
            else:
                return item

        if value:
            try:
                return process_value(getattr(self, value))
            except AttributeError:
                return value

    def as_meta(self, request=None):
        """
        Populates the :py:class:`~meta.views.Meta` object  with values from :py:attr:`_metadata`

        :param request: optional request object. Used to build the correct URI for linked objects
        :return: Meta object
        """
        from meta.views import Meta

        metadata = self.get_meta(request)
        meta = Meta(request=request, obj=self)
        for field, data in self._retrieve_data(request, metadata):
            setattr(meta, field, data)
        for field in ('og_title', 'twitter_title', 'gplus_title'):
            generaltitle = getattr(meta, 'title', False)
            if not getattr(meta, field, False) and generaltitle:
                setattr(meta, field, generaltitle)
        for field in ('og_description', 'twitter_description', 'gplus_description'):
            generaldesc = getattr(meta, 'description', False)
            if not getattr(meta, field, False) and generaldesc:
                setattr(meta, field, generaldesc)
        if self._schema:
            meta.schema = self.schema
        return meta

    @cached_property
    def schema(self):
        """
        Schema.org object description

        :return: dict
        """
        schema = {}
        for field, value in self._schema.items():
            if value:
                schema[field] = self._get_meta_value(field, value)
        return schema

    @contextlib.contextmanager
    def _set_request(self, request):
        """
        Context processor that sets the request on the current instance
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
        return self.get_protocol()

    def build_absolute_uri(self, url):
        """
        Return the full url for the provided url argument
        """
        request = self.get_request()
        if request:
            return request.build_absolute_uri(url)

        if not dj_settings.META_USE_SITES:
            raise RuntimeError(NEED_REQUEST_OBJECT_ERR_MSG)

        return self._get_full_url(url)

    def mainEntityOfPage(self):
        return {
            '@type': 'WebPage',
            '@id': self.build_absolute_uri(self.get_absolute_url())
        }

    @property
    def _local_key(self):
        return '%s:%s:%s' % (
            self._meta.app_label, self._meta.model_name, self.pk
        )
