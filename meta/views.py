from __future__ import unicode_literals

import json
from datetime import date

from django.core.exceptions import ImproperlyConfigured

from . import settings

# This global variable is used to cache schemas for visited models to avoid recursion errors when traversing
# when parent and its children has a reference to each other
# When one objects if visited, its schema is put there, in a key generated from its pk
# By adding here visited items, it can be used as a local cache, to stop recursion
visited = {}


class FullUrlMixin(object):
    """
    Provides a few convenience methods to retrieve the full URL (which includes protocol and domain) of an object.

    If possible, :py:meth:`django.http.request.HttpRequest.build_absolute_uri` is used
    """

    def get_domain(self):
        """
        Discover the current website domain

        :py:class:`django.contrib.sites.models.Site`
        and :ref:`META_SITE_DOMAIN`
        (in this order) are used

        :return: domain URL
        """
        from django.contrib.sites.models import Site
        try:
            if self.use_sites:
                return Site.objects.get_current(self.request).domain
        except AttributeError:
            if settings.USE_SITES:
                try:
                    return Site.objects.get_current(self.request).domain
                except AttributeError:
                    return Site.objects.get_current().domain
        if not settings.SITE_DOMAIN:
            raise ImproperlyConfigured('META_SITE_DOMAIN is not set')
        return settings.SITE_DOMAIN

    def get_protocol(self):
        """
        Discover the current website protocol from  :ref:`META_SITE_PROTOCOL`

        :return: domain URL
        """
        if not settings.SITE_PROTOCOL:
            raise ImproperlyConfigured('META_SITE_PROTOCOL is not set')
        return settings.SITE_PROTOCOL

    def _get_full_url(self, url):
        """
        Build the full URL (protocol and domain included) for the URL given as argument

        :param url: absolute (domain-less) URL
        :return: full url
        """
        try:
            return self.request.build_absolute_uri(url)
        except AttributeError:
            pass
        if not url:
            return None
        if url.startswith('http'):
            return url
        meta_protocol = self.get_protocol()
        domain = self.get_domain()
        separator = '://'
        if url.startswith('//'):
            separator = ':'
            domain = ''
        elif not url.startswith('/'):
            url = '/%s' % url
        if domain.startswith('http'):
            meta_protocol = ''
            separator = ''
        return '{meta_protocol}{separator}{domain}{url}'.format(
            meta_protocol=meta_protocol,
            separator=separator,
            domain=domain,
            url=url
        )


class Meta(FullUrlMixin):
    """
    Helper for building context meta object
    """
    _keywords = []
    _url = None
    _image = None
    _schema = {}
    """
    Base schema.org types definition.

    It's a dictionary containing all the schema.org properties for the described objects.

    See :ref:`a sample implementation <schema._schema>`.
    """
    request = None
    _obj = None
    """
    Linked :py:class:`~meta.models.ModelMeta` instance (if Meta is generated from a ModelMeta object)
    """

    def __init__(self, **kwargs):
        self.use_sites = kwargs.get('use_sites', settings.USE_SITES)
        self.title = kwargs.get('title')
        self.og_title = kwargs.get('og_title')
        self.twitter_title = kwargs.get('twitter_title')
        self.gplus_title = kwargs.get('gplus_title')
        self.description = kwargs.get('description')
        self.extra_props = kwargs.get('extra_props')
        self.extra_custom_props = kwargs.get('extra_custom_props')
        self.custom_namespace = kwargs.get('custom_namespace', settings.OG_NAMESPACES)
        self.keywords = kwargs.get('keywords')
        self.url = kwargs.get('url')
        self.image = kwargs.get('image')
        self.image_width = kwargs.get('image_width')
        self.image_height = kwargs.get('image_height')
        self.object_type = kwargs.get('object_type', settings.SITE_TYPE)
        self.site_name = kwargs.get('site_name', settings.SITE_NAME)
        self.twitter_site = kwargs.get('twitter_site')
        self.twitter_creator = kwargs.get('twitter_creator')
        self.twitter_card = kwargs.get('twitter_card')
        self.facebook_app_id = kwargs.get('facebook_app_id')
        self.locale = kwargs.get('locale')
        self.use_og = kwargs.get('use_og', settings.USE_OG_PROPERTIES)
        self.use_twitter = kwargs.get('use_twitter', settings.USE_TWITTER_PROPERTIES)
        self.use_facebook = kwargs.get('use_facebook', settings.USE_FACEBOOK_PROPERTIES)
        self.use_googleplus = kwargs.get('use_googleplus', settings.USE_GOOGLEPLUS_PROPERTIES)
        self.use_json_ld = kwargs.get('use_json_ld', settings.USE_JSON_LD_SCHEMA)
        self.use_title_tag = kwargs.get('use_title_tag', settings.USE_TITLE_TAG)
        self.gplus_type = kwargs.get('gplus_type', settings.GPLUS_TYPE)
        self.gplus_publisher = kwargs.get('gplus_publisher', settings.GPLUS_PUBLISHER)
        self.gplus_author = kwargs.get('gplus_author', settings.GPLUS_AUTHOR)
        self.fb_pages = kwargs.get('fb_pages', settings.FB_PAGES)
        self.og_app_id = kwargs.get('og_app_id', settings.FB_APPID)
        self.request = kwargs.get('request', None)
        self._schema = kwargs.get('schema', {})
        self._obj = kwargs.get('obj', {})

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        if keywords is None:
            kws = settings.DEFAULT_KEYWORDS
        else:
            if not hasattr(keywords, '__iter__'):
                # Not iterable
                raise ValueError('Keywords must be an iterable')
            kws = [k for k in keywords]
            if settings.INCLUDE_KEYWORDS:
                kws += settings.INCLUDE_KEYWORDS
        seen = set()
        seen_add = seen.add
        self._keywords = [k for k in kws if k not in seen and not seen_add(k)]

    def get_full_url(self, url):
        return self._get_full_url(url)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = self._get_full_url(url)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if image is None and settings.DEFAULT_IMAGE:
            image = settings.DEFAULT_IMAGE
        if image:
            if not image.startswith('http') and not image.startswith('/'):
                image = '%s%s' % (settings.IMAGE_URL, image)
            self._image = self.get_full_url(image)

    @property
    def schema(self):
        """
        Schema.org object description.

        Items in the schema are converted in a format suitable of json encoding at this stage:

        * instances of :py:class:`~meta.views.Meta` as their schema
        * dates as isoformat
        * iterables and dicts are processed depth-first to process their items

        If no type is set :py:attr:`~meta.views.Meta.gplus_type` is used

        :return: dict
        """
        from meta.models import ModelMeta

        def process_item(item):
            if isinstance(item, Meta):
                return item.schema
            if isinstance(item, ModelMeta):
                # if not cached, object schema is generated and put into local cache
                if item._local_key not in visited:
                    visited[item._local_key] = item.as_meta(self.request).schema
                return visited[item._local_key]
            elif isinstance(item, date):
                return item.isoformat()
            elif isinstance(item, list) or isinstance(item, tuple):
                return [process_item(value) for value in item]
            elif isinstance(item, dict):
                return {itemkey: process_item(itemvalue) for itemkey, itemvalue in item.items()}
            else:
                return item

        schema = {}
        # object is immediately set here to recursion
        # if we are visiting parent -> child relation, we don't need the pointer
        # back up
        if isinstance(self._obj, ModelMeta):
            visited[self._obj._local_key] = None
        for key, val in self._schema.items():
            schema[key] = process_item(val)
        if '@type' not in schema:
            schema['@type'] = self.gplus_type
        # after generating the full schema, we can save it in the local cache for future uses
        if isinstance(self._obj, ModelMeta):
            visited[self._obj._local_key] = schema
        return schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    def as_json_ld(self):
        """
        Convert the schema to json-ld

        :return: json
        """
        data = self.schema
        data['@context'] = 'http://schema.org'
        return json.dumps(data)


class MetadataMixin(FullUrlMixin):
    """
    Django CBV mixin to prepare metadata for the view context
    """
    meta_class = Meta
    context_meta_name = 'meta'

    title = None
    og_title = None
    twitter_title = None
    gplus_title = None
    description = None
    extra_props = None
    extra_custom_props = None
    custom_namespace = None
    keywords = []
    url = None
    image = None
    object_type = None
    site_name = None
    twitter_site = None
    twitter_creator = None
    twitter_card = None
    facebook_app_id = None
    locale = None
    use_sites = False
    use_og = False
    use_title_tag = False
    gplus_type = None
    gplus_author = None
    gplus_publisher = None
    schema = {}

    def __init__(self, **kwargs):
        self.use_sites = settings.USE_SITES
        self.use_og = settings.USE_OG_PROPERTIES
        self.use_title_tag = settings.USE_TITLE_TAG
        super(MetadataMixin, self).__init__(**kwargs)

    def get_meta_class(self):
        return self.meta_class

    def get_protocol(self):
        return settings.SITE_PROTOCOL

    def get_domain(self):
        return settings.SITE_DOMAIN

    def get_meta_title(self, context=None):
        return self.title

    def get_meta_og_title(self, context=None):
        return self.og_title

    def get_meta_twitter_title(self, context=None):
        return self.twitter_title

    def get_meta_gplus_title(self, context=None):
        return self.gplus_title

    def get_meta_description(self, context=None):
        return self.description

    def get_meta_keywords(self, context=None):
        return self.keywords

    def get_meta_url(self, context=None):
        return self.url

    def get_meta_image(self, context=None):
        return self.image

    def get_meta_object_type(self, context=None):
        return self.object_type or settings.SITE_TYPE

    def get_meta_site_name(self, context=None):
        return self.site_name or settings.SITE_NAME

    def get_meta_extra_props(self, context=None):
        return self.extra_props

    def get_meta_extra_custom_props(self, context=None):
        return self.extra_custom_props

    def get_meta_custom_namespace(self, context=None):
        return self.custom_namespace or settings.OG_NAMESPACES

    def get_meta_twitter_site(self, context=None):
        return self.twitter_site

    def get_meta_twitter_creator(self, context=None):
        return self.twitter_creator

    def get_meta_twitter_card(self, context=None):
        return self.twitter_card

    def get_meta_facebook_app_id(self, context=None):
        return self.facebook_app_id

    def get_meta_gplus_type(self, context=None):
        return self.gplus_type

    def get_meta_gplus_author(self, context=None):
        return self.gplus_author

    def get_meta_gplus_publisher(self, context=None):
        return self.gplus_publisher

    def get_meta_locale(self, context=None):
        return self.locale

    def get_schema(self, context=None):
        """
        The generic API to retrieve the full schema.org structure for the view.

        By default it returns the :py:attr:`schema`. You can reimplement this method
        to build the schema.org structure at runtime. See :ref:`a sample implementation <schema.get_schema>`.

        :param context: view context
        :return: dictionary
        """
        return self.schema

    def get_schema_property(self, schema_type, property, context=None):
        """
        The generic API to retrieve the attribute value for a generic schema type

        This is just a stub that **must** be implemented

        :param schema_type: name of the schema type
        :param property: name of the property
        :param context: view context
        :return: property value
        """
        raise NotImplementedError

    def get_meta(self, context=None):
        return self.get_meta_class()(
            use_og=self.use_og,
            use_title_tag=self.use_title_tag,
            use_sites=self.use_sites,
            title=self.get_meta_title(context=context),
            og_title=self.get_meta_og_title(context=context),
            twitter_title=self.get_meta_twitter_title(context=context),
            gplus_title=self.get_meta_gplus_title(context=context),
            description=self.get_meta_description(context=context),
            extra_props=self.get_meta_extra_props(context=context),
            extra_custom_props=self.get_meta_extra_custom_props(context=context),
            custom_namespace=self.get_meta_custom_namespace(context=context),
            keywords=self.get_meta_keywords(context=context),
            image=self.get_meta_image(context=context),
            url=self.get_meta_url(context=context),
            object_type=self.get_meta_object_type(context=context),
            site_name=self.get_meta_site_name(context=context),
            twitter_site=self.get_meta_twitter_site(context=context),
            twitter_creator=self.get_meta_twitter_creator(context=context),
            twitter_card=self.get_meta_twitter_card(context=context),
            locale=self.get_meta_locale(context=context),
            facebook_app_id=self.get_meta_facebook_app_id(context=context),
            gplus_type=self.get_meta_gplus_type(context=context),
            gplus_author=self.get_meta_gplus_author(context=context),
            gplus_publisher=self.get_meta_gplus_publisher(context=context),
            schema=self.get_schema(context=context),
        )

    def get_context_data(self, **kwargs):
        context = super(MetadataMixin, self).get_context_data(**kwargs)
        context[self.context_meta_name] = self.get_meta(context=context)
        return context
