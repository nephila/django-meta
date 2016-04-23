# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from meta import settings
from meta.views import Meta, MetadataMixin


class MetadataMixinTestCase(TestCase):
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

        settings.SITE_TYPE = 'foo'

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

        settings.SITE_NAME = 'Foo'

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

        settings.OG_NAMESPACES = ['foo', 'bar']
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_custom_namespace(),
            ['foo', 'bar']
        )
        settings.OG_NAMESPACES = None

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

    def test_get_meta(self):
        settings.SITE_PROTOCOL = 'http'
        settings.SITE_DOMAIN = 'foo.com'
        settings.USE_SITES = False
        settings.FB_PAGES = 'fbpages'
        settings.FB_APPID = 'appid'

        m = MetadataMixin()
        m.title = 'title'
        m.description = 'description'
        m.keywords = ['foo', 'bar']
        m.url = 'some/path'
        m.image = 'images/foo.gif'

        meta_object = m.get_meta()

        self.assertTrue(type(meta_object), Meta)
        self.assertEqual(
            meta_object.title,
            'title'
        )
        self.assertEqual(
            meta_object.description,
            'description'
        )
        self.assertEqual(
            meta_object.url,
            'http://foo.com/some/path'
        )
        self.assertEqual(
            meta_object.keywords,
            ['foo', 'bar']
        )
        self.assertEqual(
            meta_object.image,
            'http://foo.com/static/images/foo.gif'
        )
        settings.SITE_DOMAIN = 'example.com'

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

        settings.SITE_PROTOCOL = 'http'
        settings.SITE_DOMAIN = 'foo.com'
        settings.USE_SITES = False

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

        settings.SITE_DOMAIN = 'example.com'
