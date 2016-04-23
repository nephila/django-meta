# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _

SITE_PROTOCOL = getattr(django_settings, 'META_SITE_PROTOCOL', None)
SITE_DOMAIN = getattr(django_settings, 'META_SITE_DOMAIN', None)
SITE_TYPE = getattr(django_settings, 'META_SITE_TYPE', None)
SITE_NAME = getattr(django_settings, 'META_SITE_NAME', None)
INCLUDE_KEYWORDS = getattr(django_settings, 'META_INCLUDE_KEYWORDS', [])
DEFAULT_KEYWORDS = getattr(django_settings, 'META_DEFAULT_KEYWORDS', [])
IMAGE_URL = getattr(django_settings, 'META_IMAGE_URL', django_settings.STATIC_URL)
USE_OG_PROPERTIES = getattr(django_settings, 'META_USE_OG_PROPERTIES', False)
USE_TWITTER_PROPERTIES = getattr(django_settings, 'META_USE_TWITTER_PROPERTIES', False)
USE_FACEBOOK_PROPERTIES = getattr(django_settings, 'META_USE_FACEBOOK_PROPERTIES', False)
USE_GOOGLEPLUS_PROPERTIES = getattr(django_settings, 'META_USE_GOOGLEPLUS_PROPERTIES', False)
USE_SITES = getattr(django_settings, 'META_USE_SITES', False)
USE_TITLE_TAG = getattr(django_settings, 'META_USE_TITLE_TAG', False)
OG_NAMESPACES = getattr(django_settings, 'META_OG_NAMESPACES', None)

OBJECT_TYPES = (
    ('Article', _('Article')),
    ('Website', _('Website')),
)
TWITTER_TYPES = (
    ('summary', _('Summary Card')),
    ('summary_large_image', _('Summary Card with Large Image')),
    ('product', _('Product')),
    ('photo', _('Photo')),
    ('player', _('Player')),
    ('app', _('App')),
)
FB_TYPES = OBJECT_TYPES
GPLUS_TYPES = (
    ('Article', _('Article')),
    ('Blog', _('Blog')),
    ('WebPage', _('Page')),
    ('WebSite', _('WebSite')),
    ('Event', _('Event')),
    ('Product', _('Product')),
    ('Place', _('Place')),
    ('Person', _('Person')),
    ('Book', _('Book')),
    ('LocalBusiness', _('LocalBusiness')),
    ('Organization', _('Organization')),
    ('Review', _('Review')),
)


DEFAULT_IMAGE = getattr(django_settings, 'META_DEFAULT_IMAGE', '')
DEFAULT_TYPE = getattr(django_settings, 'META_SITE_TYPE', OBJECT_TYPES[0][0])
FB_TYPE = getattr(django_settings, 'META_FB_TYPE', OBJECT_TYPES[0][0])
FB_TYPES = getattr(django_settings, 'META_FB_TYPES', FB_TYPES)
FB_APPID = getattr(django_settings, 'META_FB_APPID', '')
FB_PROFILE_ID = getattr(django_settings, 'META_FB_PROFILE_ID', '')
FB_PUBLISHER = getattr(django_settings, 'META_FB_PUBLISHER', '')
FB_AUTHOR_URL = getattr(django_settings, 'META_FB_AUTHOR_URL', '')
FB_PAGES = getattr(django_settings, 'META_FB_PAGES', '')
TWITTER_TYPE = getattr(django_settings, 'META_TWITTER_TYPE', TWITTER_TYPES[0][0])
TWITTER_TYPES = getattr(django_settings, 'META_TWITTER_TYPES', TWITTER_TYPES)
TWITTER_SITE = getattr(django_settings, 'META_TWITTER_SITE', '')
TWITTER_AUTHOR = getattr(django_settings, 'META_TWITTER_AUTHOR', '')
GPLUS_TYPE = getattr(django_settings, 'META_GPLUS_TYPE', GPLUS_TYPES[0][0])
GPLUS_TYPES = getattr(django_settings, 'META_GPLUS_TYPES', GPLUS_TYPES)
GPLUS_AUTHOR = getattr(django_settings, 'META_GPLUS_AUTHOR', '')
