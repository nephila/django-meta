from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import meta
from meta.views import MetadataMixin, Meta


class MetadataMixinTestCase(unittest.TestCase):
    def test_get_meta_class(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_class(),
            Meta
        )

    def test_get_meta_title(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_title(),
            None
        )

        m.title = 'Foo'
        self.assertEqual(
            m.get_meta_title(),
            'Foo'
        )

    def test_get_meta_description(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_description(),
            None
        )

        m.description = 'Foo'
        self.assertEqual(
            m.get_meta_description(),
            'Foo'
        )

    def test_get_meta_url(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_url(),
            None
        )

        m.url = '/foo/bar'
        self.assertEqual(
            m.get_meta_url(),
            '/foo/bar'
        )

    def test_get_meta_image(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_image(),
            None
        )

        m.image = 'img/foo.gif'

        self.assertEqual(
            m.get_meta_image(),
            'img/foo.gif'
        )

    def test_get_meta_object_tye(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_object_type(),
            None
        )

        m.object_type = 'bar'
        self.assertEqual(
            m.get_meta_object_type(),
            'bar'
        )

    def test_get_meta_object_type_with_setting(self):
        m = MetadataMixin()

        meta.settings.SITE_TYPE = 'foo'

        self.assertEqual(
            m.get_meta_object_type(),
            'foo'
        )

    def test_get_meta_site_name(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_site_name(),
            None
        )

        m.site_name = 'Foo'
        self.assertEqual(
            m.get_meta_site_name(),
            'Foo'
        )

    def test_get_meta_site_name_with_setting(self):
        m = MetadataMixin()

        meta.settings.SITE_NAME = 'Foo'

        self.assertEqual(
            m.get_meta_site_name(),
            'Foo'
        )

    def test_get_meta_extra_props(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_extra_props(),
            None
        )

        m.extra_props = {
            'app_name': 'Foo',
            'app_id': 'Bar'
        }
        self.assertEqual(
            m.get_meta_extra_props(),
            {
                'app_name': 'Foo',
                'app_id': 'Bar'
            }
        )

    def test_get_meta_extra_custom_props(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_extra_custom_props(),
            None
        )

        m.extra_custom_props = [
            ('property', 'app_name', 'Foo'),
            ('property', 'app_id', 'Bar'),
        ]
        self.assertEqual(
            m.get_meta_extra_custom_props(),
            [
                ('property', 'app_name', 'Foo'),
                ('property', 'app_id', 'Bar'),
            ]
        )

    def test_get_meta_custom_namespace(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_custom_namespace(),
            None
        )

        m.custom_namespace = "my-website"
        self.assertEqual(
            m.get_meta_custom_namespace(),
            'my-website'
        )

    def test_get_meta_twitter_site(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_twitter_site(),
            None
        )

        m.twitter_site = '@foo'
        self.assertEqual(
            m.get_meta_twitter_site(),
            '@foo'
        )

    def test_get_meta_twitter_creator(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_twitter_creator(),
            None
        )

        m.twitter_creator = '@foo'
        self.assertEqual(
            m.get_meta_twitter_creator(),
            '@foo'
        )

    def test_get_meta_twitter_card(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_twitter_card(),
            None
        )

        m.twitter_card = 'summary'
        self.assertEqual(
            m.get_meta_twitter_card(),
            'summary'
        )

    def test_get_meta_facebook_app_id(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_facebook_app_id(),
            None
        )

        m.facebook_app_id = '12345'
        self.assertEqual(
            m.get_meta_facebook_app_id(),
            '12345'
        )

    def test_get_meta_locale(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_locale(),
            None
        )

        m.locale = 'en_US'
        self.assertEqual(
            m.get_meta_locale(),
            'en_US'
        )

    def test_get_context(self):
        class Super(object):
            def get_context_data(self):
                return {}

        class View(MetadataMixin, Super):
            title = 'title'
            description = 'description'
            keywords = ['foo', 'bar']
            url = 'some/path'
            image = 'images/foo.gif'

        meta.settings.SITE_PROTOCOL = 'http'
        meta.settings.SITE_DOMAIN = 'foo.com'

        v = View()

        context = v.get_context_data()

        self.assertTrue('meta' in context)
        self.assertTrue(type(context['meta']), Meta)
        self.assertEqual(
            context['meta'].url,
            'http://foo.com/some/path'
        )
        self.assertEqual(
            context['meta'].keywords,
            ['foo', 'bar']
        )
        self.assertEqual(
            context['meta'].image,
            'http://foo.com/static/images/foo.gif'
        )
