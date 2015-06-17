from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from meta.views import Meta
from meta.templatetags.meta import (
    og_prop, meta, meta_list, twitter_prop, generic_prop,
    googleplus_prop, googleplus_html_scope, custom_meta,
    custom_meta_extras, meta_extras, facebook_prop, meta_namespaces)


class OgPropTestCase(unittest.TestCase):
    def test_og_prop_basically_works(self):
        self.assertEqual(
            og_prop('type', 'website'),
            '<meta property="og:type" content="website">'
        )
    def test_generic_prop_basically_works(self):
        self.assertEqual(
            generic_prop('og', 'type', 'website'),
            '<meta property="og:type" content="website">'
        )


class MetaTestCase(unittest.TestCase):
    def test_meta_basically_works(self):
        self.assertEqual(
            meta('description', 'Awesome website about ponies'),
            '<meta name="description" content="Awesome website about ponies">'
        )


class CustomMetaTestCase(unittest.TestCase):
    def test_custom_meta_basically_works(self):
        self.assertEqual(
            custom_meta('property', 'foo', 'bar'),
            '<meta property="foo" content="bar">'
        )


class TwitterPropTestCase(unittest.TestCase):
    def test_twitter_basically_works(self):
        self.assertEqual(
            twitter_prop('foo', 'bar'),
            '<meta name="twitter:foo" content="bar">'
        )


class FacebookPropTestCase(unittest.TestCase):
    def test_facebook_basically_works(self):
        self.assertEqual(
            facebook_prop('foo', 'bar'),
            '<meta name="fb:foo" content="bar">'
        )


class GooglePlusPropTestcase(unittest.TestCase):
    def test_google_plus_basically_wors(self):
        self.assertEqual(
            googleplus_prop('foo', 'bar'),
            '<meta itemprop="foo" content="bar">'
        )
        
    def test_google_plus_scope_works(self):
        self.assertEqual(
            googleplus_html_scope('bar'),
            ' itemscope itemtype="http://schema.org/bar" '
        )


class MetaListTestCase(unittest.TestCase):
    def test_meta_list_basically_works(self):
        self.assertEqual(
            meta_list('keywords', ['foo', 'bar', 'baz']),
            '<meta name="keywords" content="foo, bar, baz">'
        )

    def test_meta_list_with_non_list_value(self):
        self.assertEqual(
            meta_list('keywords', 12),
            ''
        )


class MetaExtrasTestCase(unittest.TestCase):
    def test_meta_extras_basically_works(self):
        result = meta_extras({
            'type': 'foo',
            'image_width': 'bar'
        })
        self.assertTrue('<meta name="type" content="foo">' in result)
        self.assertTrue('<meta name="image_width" content="bar">' in result)


class CustomMetaExtrasTestCase(unittest.TestCase):
    def test_custom_meta_extras_basically_works(self):
        result = custom_meta_extras([
                ('property', 'type', 'foo'),
                ('key', 'image_width', 'bar')
        ])
        self.assertTrue('<meta property="type" content="foo">' in result)
        self.assertTrue('<meta key="image_width" content="bar">' in result)


class MetaNamespaceTestCase(unittest.TestCase):
    def test_meta_namespaces_no_meta_in_context(self):
        context = {}
        result = meta_namespaces(context)
        expected = ''
        self.assertEqual(result, expected)

    def test_meta_namespaces_default(self):
        context = {
            'meta': Meta()
        }
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_facebook(self):
        context = {
            'meta': Meta(use_facebook=True)
        }
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_custom(self):
        context = {
            'meta': Meta(custom_namespace='my-website')
        }
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# my-website: http://ogp.me/ns/my-website#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_facebook_and_custom(self):
        context = {
            'meta': Meta(use_facebook=True, custom_namespace='my-website')
        }
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# my-website: http://ogp.me/ns/my-website#"'
        self.assertEqual(result, expected)
