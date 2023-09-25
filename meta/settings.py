from django.conf import settings as django_settings
from django.utils.translation import gettext_lazy as _

META_SITE_PROTOCOL = None
META_SITE_DOMAIN = None
META_SITE_TYPE = None
META_SITE_NAME = None
META_INCLUDE_KEYWORDS = []
META_DEFAULT_KEYWORDS = []
META_IMAGE_URL = django_settings.STATIC_URL
META_USE_OG_PROPERTIES = False
META_USE_TWITTER_PROPERTIES = False
META_USE_FACEBOOK_PROPERTIES = False
META_USE_SCHEMAORG_PROPERTIES = False
META_USE_JSON_LD_SCHEMA = False
META_USE_SITES = False
META_USE_TITLE_TAG = False
META_OG_NAMESPACES = None


OBJECT_TYPES = (
    ("Article", _("Article")),
    ("Website", _("Website")),
)
TWITTER_TYPES = (
    ("summary", _("Summary Card")),
    ("summary_large_image", _("Summary Card with Large Image")),
    ("product", _("Product")),
    ("photo", _("Photo")),
    ("player", _("Player")),
    ("app", _("App")),
)
FB_TYPES = OBJECT_TYPES
SCHEMAORG_TYPES = (
    ("Article", _("Article")),
    ("Blog", _("Blog")),
    ("WebPage", _("Page")),
    ("WebSite", _("WebSite")),
    ("Event", _("Event")),
    ("Product", _("Product")),
    ("Place", _("Place")),
    ("Person", _("Person")),
    ("Book", _("Book")),
    ("LocalBusiness", _("LocalBusiness")),
    ("Organization", _("Organization")),
    ("Review", _("Review")),
)

META_OG_SECURE_URL_ITEMS = ("image", "audio", "video")
META_DEFAULT_IMAGE = ""
META_DEFAULT_TYPE = OBJECT_TYPES[0][0]
META_FB_TYPE = OBJECT_TYPES[0][0]
META_FB_TYPES = FB_TYPES
META_FB_APPID = ""
META_FB_PROFILE_ID = ""
META_FB_PUBLISHER = ""
META_FB_AUTHOR_URL = ""
META_FB_PAGES = ""
META_TWITTER_TYPE = TWITTER_TYPES[0][0]
META_TWITTER_TYPES = TWITTER_TYPES
META_TWITTER_SITE = ""
META_TWITTER_AUTHOR = ""
META_SCHEMAORG_TYPE = SCHEMAORG_TYPES[0][0]
META_SCHEMAORG_TYPES = SCHEMAORG_TYPES

params = {param: value for param, value in locals().items() if param.startswith("META_")}


def get_setting(name):
    """Get setting value from django settings with fallback to globals defaults."""
    from django.conf import settings

    return getattr(settings, "META_%s" % name, params["META_%s" % name])
