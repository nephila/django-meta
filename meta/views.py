import warnings

from django.core.exceptions import ImproperlyConfigured

from . import settings


class Meta:
    """
    Helper for building context meta object
    """

    _keywords = []
    _url = None
    _image = None
    _image_object = None
    request = None

    def __init__(self, **kwargs):
        self.use_sites = kwargs.get("use_sites", settings.USE_SITES)
        self.title = kwargs.get("title")
        self.og_title = kwargs.get("og_title")
        self.twitter_title = kwargs.get("twitter_title")
        self.schemaorg_title = kwargs.get("schemaorg_title")
        self.description = kwargs.get("description")
        self.extra_props = kwargs.get("extra_props")
        self.extra_custom_props = kwargs.get("extra_custom_props")
        self.custom_namespace = kwargs.get("custom_namespace", settings.OG_NAMESPACES)
        self.keywords = kwargs.get("keywords")
        self.url = kwargs.get("url")
        self.image = kwargs.get("image")
        self.image_object = kwargs.get("image_object")
        self.image_width = kwargs.get("image_width")
        self.image_height = kwargs.get("image_height")
        self.object_type = kwargs.get("object_type", settings.SITE_TYPE)
        self.site_name = kwargs.get("site_name", settings.SITE_NAME)
        self.twitter_site = kwargs.get("twitter_site")
        self.twitter_creator = kwargs.get("twitter_creator")
        self.twitter_type = kwargs.get("twitter_type", kwargs.get("twitter_card", settings.TWITTER_TYPE))
        self.twitter_card = self.twitter_type
        self.facebook_app_id = kwargs.get("facebook_app_id")
        self.locale = kwargs.get("locale")
        self.use_og = kwargs.get("use_og", settings.USE_OG_PROPERTIES)
        self.use_twitter = kwargs.get("use_twitter", settings.USE_TWITTER_PROPERTIES)
        self.use_facebook = kwargs.get("use_facebook", settings.USE_FACEBOOK_PROPERTIES)
        self.use_schemaorg = kwargs.get("use_schemaorg", settings.USE_SCHEMAORG_PROPERTIES)
        self.use_title_tag = kwargs.get("use_title_tag", settings.USE_TITLE_TAG)
        self.schemaorg_type = kwargs.get("schemaorg_type", settings.SCHEMAORG_TYPE)
        self.fb_pages = kwargs.get("fb_pages", settings.FB_PAGES)
        self.og_app_id = kwargs.get("og_app_id", settings.FB_APPID)
        self.request = kwargs.get("request", None)

    def get_domain(self):
        if self.use_sites:
            from django.contrib.sites.models import Site

            return Site.objects.get_current(self.request).domain
        if not settings.SITE_DOMAIN:
            raise ImproperlyConfigured("META_SITE_DOMAIN is not set")
        return settings.SITE_DOMAIN

    def get_protocol(self):
        if not settings.SITE_PROTOCOL:
            raise ImproperlyConfigured("META_SITE_PROTOCOL is not set")
        return settings.SITE_PROTOCOL

    def get_full_url(self, url):
        if not url:
            return None
        if url.startswith("http"):
            return url
        if url.startswith("//"):
            return "{}:{}".format(self.get_protocol(), url)
        if url.startswith("/"):
            return "{}://{}{}".format(self.get_protocol(), self.get_domain(), url)
        return "{}://{}/{}".format(self.get_protocol(), self.get_domain(), url)

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        if keywords is None:
            kws = settings.DEFAULT_KEYWORDS
        else:
            if not hasattr(keywords, "__iter__"):
                # Not iterable
                raise ValueError("Keywords must be an intrable")
            kws = list(keywords)
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

    def _normalize_media_url(self, url):
        if not url.startswith("http") and not url.startswith("/"):
            url = "{}{}".format(settings.IMAGE_URL, url)
        return self.get_full_url(url)

    @property
    def image(self):
        if self.image_object:
            return self.image_object.get("url")
        else:
            return self._image

    @image.setter
    def image(self, image):
        if image is None and settings.DEFAULT_IMAGE:
            image = settings.DEFAULT_IMAGE
        if image:
            self._image = self._normalize_media_url(image)

    @property
    def image_object(self):
        return self._image_object

    @image_object.setter
    def image_object(self, image):
        try:
            if image:
                image["url"] = self._normalize_media_url(image.get("url", None))
                if self.get_protocol() == "https":
                    secure_fallback_url = image.get("secure_url", image.get("url", None))
                    image["secure_url"] = self._normalize_media_url(secure_fallback_url)
                    if image["secure_url"].startswith("http://"):
                        image["secure_url"] = image["secure_url"].replace("http://", "https://")
                self._image_object = image
        except KeyError:
            self._image_object = None


class MetadataMixin:
    """
    Django CBV mixin to prepare metadata for the view context
    """

    meta_class = Meta
    context_meta_name = "meta"

    title = None
    og_title = None
    twitter_title = None
    schemaorg_title = None
    description = None
    extra_props = None
    extra_custom_props = None
    custom_namespace = None
    keywords = []
    url = None
    image = None
    image_object = None
    object_type = None
    site_name = None
    twitter_site = None
    twitter_creator = None
    twitter_type = None
    facebook_app_id = None
    locale = None
    use_sites = False
    use_og = False
    use_title_tag = False
    schemaorg_type = None

    def __init__(self, **kwargs):
        self.use_sites = settings.USE_SITES
        self.use_og = settings.USE_OG_PROPERTIES
        self.use_title_tag = settings.USE_TITLE_TAG
        super().__init__(**kwargs)

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

    def get_meta_schemaorg_title(self, context=None):
        return self.schemaorg_title

    def get_meta_description(self, context=None):
        return self.description

    def get_meta_keywords(self, context=None):
        return self.keywords

    def get_meta_url(self, context=None):
        return self.url

    def get_meta_image(self, context=None):
        if self.image_object and self.image_object.get("url", None):
            return self.image_object["url"]
        return self.image

    def get_meta_image_object(self, context=None):
        return self.image_object

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

    @property
    def twitter_card(self):
        warnings.warn("twitter_card attribute will be removed in version 3.0", PendingDeprecationWarning, stacklevel=2)
        return self.twitter_type

    @twitter_card.setter
    def twitter_card(self, value):
        warnings.warn("twitter_card attribute will be removed in version 3.0", PendingDeprecationWarning, stacklevel=2)
        self.twitter_type = value

    def get_meta_twitter_card(self, context=None):
        warnings.warn(
            "get_meta_twitter_card attribute will be removed in version 3.0", PendingDeprecationWarning, stacklevel=2
        )
        return self.twitter_type

    def get_meta_twitter_type(self, context=None):
        return self.twitter_type

    def get_meta_facebook_app_id(self, context=None):
        return self.facebook_app_id

    def get_meta_schemaorg_type(self, context=None):
        return self.schemaorg_type

    def get_meta_locale(self, context=None):
        return self.locale

    def get_meta(self, context=None):
        return self.get_meta_class()(
            use_og=self.use_og,
            use_title_tag=self.use_title_tag,
            use_sites=self.use_sites,
            title=self.get_meta_title(context=context),
            og_title=self.get_meta_og_title(context=context),
            twitter_title=self.get_meta_twitter_title(context=context),
            schemaorg_title=self.get_meta_schemaorg_title(context=context),
            description=self.get_meta_description(context=context),
            extra_props=self.get_meta_extra_props(context=context),
            extra_custom_props=self.get_meta_extra_custom_props(context=context),
            custom_namespace=self.get_meta_custom_namespace(context=context),
            keywords=self.get_meta_keywords(context=context),
            image=self.get_meta_image(context=context),
            image_object=self.get_meta_image_object(context=context),
            url=self.get_meta_url(context=context),
            object_type=self.get_meta_object_type(context=context),
            site_name=self.get_meta_site_name(context=context),
            twitter_site=self.get_meta_twitter_site(context=context),
            twitter_creator=self.get_meta_twitter_creator(context=context),
            twitter_type=self.get_meta_twitter_type(context=context),
            locale=self.get_meta_locale(context=context),
            facebook_app_id=self.get_meta_facebook_app_id(context=context),
            schemaorg_type=self.get_meta_schemaorg_type(context=context),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_meta_name] = self.get_meta(context=context)
        return context
