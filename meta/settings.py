from django.conf import settings

SITE_TYPE = getattr(settings, 'META_SITE_TYPE', None)
SITE_NAME = getattr(settings, 'META_SITE_NAME', None)
SITE_PROTOCOL = getattr(settings, 'META_SITE_PROTOCOL', 'http')
SITE_DOMAIN = getattr(settings, 'META_SITE_DOMAIN', None)
USE_OG_PROPERTIES = getattr(settings, 'META_USE_OG_PROPERTIES', False)
