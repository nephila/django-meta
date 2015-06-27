from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from django.core.exceptions import ImproperlyConfigured

import meta
from meta.views import Meta


class MetaObjectTestCase(unittest.TestCase):
    def setUp(self):
        # Set all settings back to defaults
        meta.settings.SITE_TYPE = None
        meta.settings.SITE_NAME = None
        meta.settings.SITE_PROTOCOL = None
        meta.settings.SITE_DOMAIN = None
        meta.settings.INCLUDE_KEYWORDS = []
        meta.settings.DEFAULT_KEYWORDS = []
        meta.settings.USE_OG_PROPERTIES = False
        meta.settings.IMAGE_URL = '/static/'
        meta.settings.USE_TWITTER_PROPERTIES = False
        meta.settings.USE_FACEBOOK_PROPERTIES = False
        meta.settings.USE_GOOGLEPLUS_PROPERTIES = False

    def test_defaults(self):
        m = Meta()
        self.assertEqual(m.title, None)
        self.assertEqual(m.description, None)
        self.assertEqual(m.extra_props, None)
        self.assertEqual(m.extra_custom_props, None)
        self.assertEqual(m.custom_namespace, None)
        self.assertEqual(m.keywords, [])
        self.assertEqual(m.url, None)
        self.assertEqual(m.image, None)
        self.assertEqual(m.object_type, None)
        self.assertEqual(m.site_name, None)
        self.assertEqual(m.twitter_site, None)
        self.assertEqual(m.locale, None)
        self.assertEqual(m.facebook_app_id, None)
        self.assertEqual(m.use_og, False)
        self.assertEqual(m.use_sites, False)
        self.assertEqual(m.use_twitter, False)
        self.assertEqual(m.use_facebook, False)
        self.assertEqual(m.use_googleplus, False)

    def test_set_keywords(self):
        m = Meta(keywords = ['foo', 'bar'])
        self.assertEqual(m.keywords[0], 'foo')
        self.assertEqual(m.keywords[1], 'bar')

    def test_set_keywords_with_include(self):
        meta.settings.INCLUDE_KEYWORDS = ['baz']
        m = Meta(keywords = ['foo', 'bar'])
        self.assertEqual(m.keywords[0], 'foo')
        self.assertEqual(m.keywords[1], 'bar')
        self.assertEqual(m.keywords[2], 'baz')

    def test_set_keywords_no_duplicate(self):
        m = Meta(keywords = ['foo', 'foo', 'foo'])
        self.assertEqual(m.keywords[0], 'foo')
        self.assertEqual(len(m.keywords), 1)

    def test_set_keywords_with_defaults(self):
        meta.settings.DEFAULT_KEYWORDS = ['foo', 'bar']
        m = Meta()
        self.assertEqual(m.keywords[0], 'foo')
        self.assertEqual(m.keywords[1], 'bar')

    def test_get_full_url_with_None(self):
        m = Meta()
        self.assertEqual(m.get_full_url(None), None)

    def test_get_full_url_with_full_url(self):
        m = Meta()
        self.assertEqual(
            m.get_full_url('http://example.com/foo'),
            'http://example.com/foo'
        )

    def test_get_full_url_without_protocol_will_raise(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url('foo/bar')

    def test_get_full_url_without_domain_will_raise(self):
        meta.settings.SITE_PROTOCOL = 'http'
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url('foo/bar')

    def test_get_full_url_with_domain_and_protocol(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        m = Meta()
        self.assertEqual(
            m.get_full_url('foo/bar'),
            'https://foo.com/foo/bar'
        )

    def test_get_full_url_with_absolute_path(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        m = Meta()
        self.assertEqual(
            m.get_full_url('/foo/bar'),
            'https://foo.com/foo/bar'
        )

    def test_set_url(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        m = Meta(url='foo/bar')
        self.assertEqual(m.url, 'https://foo.com/foo/bar')

    def test_set_image_with_full_url(self):
        m = Meta(image='http://meta.example.com/image.gif')
        self.assertEqual(m.image, 'http://meta.example.com/image.gif')

    def test_set_image_with_absolute_path(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        m = Meta(image='/img/image.gif')
        self.assertEqual(m.image, 'https://foo.com/img/image.gif')

    def test_set_image_with_relative_path(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        m = Meta(image='img/image.gif')
        self.assertEqual(m.image, 'https://foo.com/static/img/image.gif')

    def test_set_image_with_image_url(self):
        meta.settings.SITE_PROTOCOL = 'https'
        meta.settings.SITE_DOMAIN = 'foo.com'
        meta.settings.IMAGE_URL = '/thumb/'
        m = Meta(image='img/image.gif')
        self.assertEqual(m.image, 'https://foo.com/thumb/img/image.gif')

