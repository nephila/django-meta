from django.conf import settings

SITE_PROTOCOL = getattr(settings, 'META_SITE_PROTOCOL', None)
SITE_DOMAIN = getattr(settings, 'META_SITE_DOMAIN', None)
SITE_TYPE = getattr(settings, 'META_SITE_TYPE', None)
SITE_NAME = getattr(settings, 'META_SITE_NAME', None)
INCLUDE_KEYWORDS = getattr(settings, 'META_INCLUDE_KEYWORDS', [])
DEFAULT_KEYWORDS = getattr(settings, 'META_DEFAULT_KEYWORDS', [])
IMAGE_URL = getattr(settings, 'META_IMAGE_URL', settings.STATIC_URL)
USE_OG_PROPERTIES = getattr(settings, 'META_USE_OG_PROPERTIES', False)
USE_SITES = getattr(settings, 'META_USE_SITES', False)
