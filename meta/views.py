from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings as django_settings

from . import settings


class Meta(object):
    """ Helper for building context meta object """

    _keywords = []
    _url = None
    _image = None

    def __init__(self, **kwargs):
        self.use_sites = kwargs.get('use_sites', settings.USE_SITES)
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.keywords = kwargs.get('keywords')
        self.url = kwargs.get('url')
        self.image = kwargs.get('image')
        self.object_type = kwargs.get('object_type', settings.SITE_TYPE)
        self.site_name = kwargs.get('site_name', settings.SITE_NAME)
        self.use_og = kwargs.get('use_og', settings.USE_OG_PROPERTIES)

    def get_domain(self):
        if self.use_sites:
            from django.contrib.sites.models import Site
            return Site.objects.get_current().domain
        if not settings.SITE_DOMAIN:
            raise ImproperlyConfigured('META_SITE_DOMAIN is not set')
        return settings.SITE_DOMAIN

    def get_protocol(self):
        if not settings.SITE_PROTOCOL:
            raise ImproperlyConfigured('META_SITE_PROTOCOL is not set')
        return settings.SITE_PROTOCOL

    def get_full_url(self, url):
        if not url:
            return None
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return '%s://%s%s' % (
                self.get_protocol(),
                self.get_domain(),
                url
            )
        return '%s://%s/%s' % (
            self.get_protocol(),
            self.get_domain(),
            url
        )

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
                raise ValueError('Keywords must be an intrable')
            kws = [k for k in keywords]
            if settings.INCLUDE_KEYWORDS:
                kws += settings.INCLUDE_KEYWORDS
        seen = set()
        seen_add = seen.add
        self._keywords = [k for k in kws if k not in seen and not seen_add(k)]

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = self.get_full_url(url)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        if image is None:
            self._image = None
            return
        if not image.startswith('http') and not image.startswith('/'):
            image = '%s%s' % (settings.IMAGE_URL, image)
        self._image = self.get_full_url(image)


class MetadataMixin(object):
    """ Django CBV mixin to prepare metadata for the view context """

    meta_class = Meta
    title = None
    description = None
    keywords = []
    url = None
    image = None
    object_type = None
    site_name = None
    use_sites = settings.USE_SITES
    use_og = settings.USE_OG_PROPERTIES

    def get_meta_class(self):
        return self.meta_class

    def get_protocol(self):
        return settings.SITE_PROTOCOL

    def get_domain(self):
        return settings.SITE_DOMAIN

    def get_meta_title(self, context={}):
        return self.title

    def get_meta_description(self, context={}):
        return self.description

    def get_meta_keywords(self, context={}):
        return self.keywords

    def get_meta_url(self, context={}):
        return self.url

    def get_meta_image(self, context={}):
        return self.image

    def get_meta_object_type(self, context={}):
        return self.object_type or settings.SITE_TYPE

    def get_meta_site_name(self, context={}):
        return self.site_name or settings.SITE_NAME

    def get_context_data(self, **kwargs):
        context = super(MetadataMixin, self).get_context_data(**kwargs)
        context['meta'] = self.get_meta_class()(
            use_og=self.use_og,
            use_sites=self.use_sites,
            title=self.get_meta_title(context=context),
            description=self.get_meta_description(context=context),
            keywords=self.get_meta_keywords(context=context),
            image=self.get_meta_image(context=context),
            url=self.get_meta_url(context=context),
            object_type=self.get_meta_object_type(context=context),
            site_name=self.get_meta_site_name(context=context),
        )
        return context
