from __future__ import unicode_literals

import unittest

import meta
from meta.views import MetadataMixin


class MetadataMixinTestCase(unittest.TestCase):
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

    def test_get_meta_url_with_full_url(self):
        m = MetadataMixin()
        m.url = 'http://example.com/some/path'
        self.assertEqual(
            m.get_meta_url(),
            'http://example.com/some/path'
        )

    def test_get_meta_url_with_absolute_path(self):
        m = MetadataMixin()
        m.url = '/some/path'

        meta.settings.SITE_DOMAIN = 'foo.com'

        self.assertEqual(
            m.get_meta_url(),
            'http://foo.com/some/path'
        )

    def test_get_meta_url_with_relative_path(self):
        m = MetadataMixin()
        m.url = 'some/path'

        meta.settings.SITE_DOMAIN = 'foo.com'

        self.assertEqual(
            m.get_meta_url(),
            'http://foo.com/some/path'
        )

    def test_get_meta_image(self):
        m = MetadataMixin()
        self.assertEqual(
            m.get_meta_image(),
            None
        )

    def test_get_meta_image_with_relative_url(self):
        m = MetadataMixin()
        m.image = 'img/foo.gif'

        meta.settings.SITE_DOMAIN = 'foo.com'

        self.assertEqual(
            m.get_meta_image(),
            'http://foo.com/static/img/foo.gif'
        )

    def test_get_meta_image_with_absolute_url(self):
        m = MetadataMixin()
        m.image = '/uploads/foo.gif'

        meta.settings.SITE_DOMAIN = 'foo.com'

        self.assertEqual(
            m.get_meta_image(),
            'http://foo.com/uploads/foo.gif'
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

    def test_get_context(self):
        class Super(object):
            def get_context_data(self):
                return {}

        class View(MetadataMixin, Super):
            title = 'title'
            description = 'description'
            url = 'some/path'
            image = 'images/foo.gif'

        meta.settings.SITE_DOMAIN = 'foo.com'

        v = View()

        context = v.get_context_data()

        self.assertTrue('meta' in context)
        self.assertEqual(context['meta']['title'], 'title')
        self.assertEqual(context['meta']['description'], 'description')
        self.assertEqual(
            context['meta']['url'],
            'http://foo.com/some/path'
        )
        self.assertEqual(
            context['meta']['image'],
            'http://foo.com/static/images/foo.gif'
        )
        self.assertEqual(
            context['meta']['use_og'],
            False
        )

