import warnings
from copy import copy

from django.conf import settings as dj_settings

from . import settings
from .utils import get_request, set_request

NEED_REQUEST_OBJECT_ERR_MSG = (
    "Meta models needs request objects when initializing if sites framework "
    "is not used. See META_USE_SITES setting."
).strip()


class ModelMeta:
    """
    Meta information mixin.
    """

    _metadata = {}
    _metadata_default = {
        "title": False,
        "og_title": False,
        "twitter_title": False,
        "schemaorg_title": False,
        "description": False,
        "og_description": False,
        "twitter_description": False,
        "schemaorg_description": False,
        "keywords": False,
        "image": settings.DEFAULT_IMAGE,
        "image_object": None,
        "image_width": False,
        "image_height": False,
        "object_type": settings.DEFAULT_TYPE,
        "og_type": settings.FB_TYPE,
        "og_app_id": settings.FB_APPID,
        "og_profile_id": settings.FB_PROFILE_ID,
        "og_publisher": settings.FB_PUBLISHER,
        "og_author_url": settings.FB_AUTHOR_URL,
        "fb_pages": settings.FB_PAGES,
        "twitter_type": settings.TWITTER_TYPE,
        "twitter_site": settings.TWITTER_SITE,
        "twitter_author": settings.TWITTER_AUTHOR,
        "schemaorg_type": settings.SCHEMAORG_TYPE,
        "published_time": False,
        "modified_time": False,
        "expiration_time": False,
        "tag": False,
        "url": False,
        "locale": False,
        "custom_namespace": settings.OG_NAMESPACES,
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
        with set_request(request):
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
            try:
                attr = getattr(self, value)
                if callable(attr):
                    try:
                        return attr(field)
                    except TypeError:
                        return attr()
                else:
                    return attr
            except (AttributeError, TypeError):
                return value

    def as_meta(self, request=None):
        """
        Method that generates the Meta object (from django-meta)
        """
        from meta.views import Meta

        metadata = self.get_meta(request)
        meta = Meta(request=request)
        for field, data in self._retrieve_data(request, metadata):
            setattr(meta, field, data)
        for field in ("og_title", "twitter_title", "schemaorg_title"):
            generaltitle = getattr(meta, "title", False)
            if not getattr(meta, field, False) and generaltitle:
                setattr(meta, field, generaltitle)
        for field in ("og_description", "twitter_description", "schemaorg_description"):
            generaldesc = getattr(meta, "description", False)
            if not getattr(meta, field, False) and generaldesc:
                setattr(meta, field, generaldesc)
        return meta

    def get_request(self):
        """
        Retrieve request from current instance
        """
        warnings.warn(
            "use meta.utils.get_request function, ModelMeta.get_request will be removed in version 3.0",
            PendingDeprecationWarning,
            stacklevel=2,
        )
        return get_request()

    def get_author(self):
        """
        Retrieve the author object. This is meant to be overridden in the model
        to return the actual author instance (e.g.: the user object).
        """

        class Author:
            fb_url = None
            twitter_profile = None
            schemaorg_profile = None

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
            return ""

    def get_author_name(self):
        """
        Sample method to return the author full name
        """
        try:
            return self.get_author().get_full_name()
        except AttributeError:  # pragma: no cover
            return ""

    def get_author_twitter(self):
        """
        Sample method to return the author twitter account
        """
        try:
            return self.get_author().twitter_profile
        except AttributeError:  # pragma: no cover
            return ""

    def get_author_schemaorg(self):
        """
        Sample method to return the author Schema.org URL
        """
        try:
            return self.get_author().schemaorg_profile
        except AttributeError:  # pragma: no cover
            return ""

    def get_meta_protocol(self):
        """
        Current http protocol
        """
        return dj_settings.META_SITE_PROTOCOL

    def build_absolute_uri(self, url):
        """
        Return the full url for the provided url argument
        """
        request = get_request()
        if request:
            return request.build_absolute_uri(url)

        if not settings.USE_SITES:
            raise RuntimeError(NEED_REQUEST_OBJECT_ERR_MSG)

        from django.contrib.sites.models import Site

        s = Site.objects.get_current()
        meta_protocol = self.get_meta_protocol()
        if url.startswith("http"):
            return url
        if s.domain.find("http") > -1:
            return "{}{}".format(s.domain, url)  # pragma: no cover
        else:
            if url.startswith("/"):
                return "{}://{}{}".format(meta_protocol, s.domain, url)
            else:
                return "{}://{}/{}".format(meta_protocol, s.domain, url)
