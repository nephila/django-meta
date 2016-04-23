from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured

from . import settings


class Meta(object):
    """
    Helper for building context meta object
    """
    _keywords = []
    _url = None
    _image = None

    def __init__(self, **kwargs):
        self.use_sites = kwargs.get('use_sites', settings.USE_SITES)
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.extra_props = kwargs.get('extra_props')
        self.extra_custom_props = kwargs.get('extra_custom_props')
        self.custom_namespace = kwargs.get('custom_namespace', settings.OG_NAMESPACES)
        self.keywords = kwargs.get('keywords')
        self.url = kwargs.get('url')
        self.image = kwargs.get('image')
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
        self.use_title_tag = kwargs.get('use_title_tag', settings.USE_TITLE_TAG)
        self.gplus_type = kwargs.get('gplus_type', settings.GPLUS_TYPE)
        self.fb_pages = kwargs.get('fb_pages', settings.FB_PAGES)
        self.og_app_id = kwargs.get('og_app_id', settings.FB_APPID)

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
        if url.startswith('//'):
            return '%s:%s' % (
                self.get_protocol(),
                url
            )
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
        if image is None and settings.DEFAULT_IMAGE:
            self._image = self.get_full_url(settings.DEFAULT_IMAGE)
            return
        elif image is None:
            self._image = None
            return
        else:
            if not image.startswith('http') and not image.startswith('/'):
                image = '%s%s' % (settings.IMAGE_URL, image)
            self._image = self.get_full_url(image)


class MetadataMixin(object):
    """
    Django CBV mixin to prepare metadata for the view context
    """
    meta_class = Meta
    context_meta_name = 'meta'

    title = None
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
    use_use_title_tag = False

    def __init__(self, **kwargs):
        self.use_sites = settings.USE_SITES
        self.use_og = settings.USE_OG_PROPERTIES
        self.use_title_tag = settings.USE_TITLE_TAG

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

    def get_meta_extra_props(self, context={}):
        return self.extra_props

    def get_meta_extra_custom_props(self, context={}):
        return self.extra_custom_props

    def get_meta_custom_namespace(self, context={}):
        return self.custom_namespace or settings.OG_NAMESPACES

    def get_meta_twitter_site(self, context={}):
        return self.twitter_site

    def get_meta_twitter_creator(self, context={}):
        return self.twitter_creator

    def get_meta_twitter_card(self, context={}):
        return self.twitter_card

    def get_meta_facebook_app_id(self, context={}):
        return self.facebook_app_id

    def get_meta_locale(self, context={}):
        return self.locale

    def get_meta(self, context={}):
        return self.get_meta_class()(
            use_og=self.use_og,
            use_title_tag=self.use_title_tag,
            use_sites=self.use_sites,
            title=self.get_meta_title(context=context),
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
        )

    def get_context_data(self, **kwargs):
        context = super(MetadataMixin, self).get_context_data(**kwargs)
        context[self.context_meta_name] = self.get_meta(context=context)
        return context
