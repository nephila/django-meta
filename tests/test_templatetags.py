import sys
import warnings

from django.test import TestCase

from meta.templatetags.meta import (
    custom_meta,
    custom_meta_extras,
    facebook_prop,
    generic_prop,
    googleplus_html_scope,
    googleplus_prop,
    googleplus_scope,
    meta,
    meta_extras,
    meta_list,
    meta_namespaces,
    meta_namespaces_gplus,
    meta_namespaces_schemaorg,
    og_prop,
    schemaorg_html_scope,
    schemaorg_prop,
    schemaorg_scope,
    title_prop,
    twitter_prop,
)
from meta.views import Meta


class OgPropTestCase(TestCase):
    def test_og_prop_basically_works(self):
        self.assertEqual(og_prop("type", "website"), '<meta property="og:type" content="website">')

    def test_og_prop_secure_url(self):
        for content in ("image", "video", "audio"):
            self.assertEqual(
                og_prop(content, "https://some/{}".format(content)),
                '<meta property="og:{0}" content="https://some/{0}">\n'
                '<meta property="og:{0}:secure_url" content="https://some/{0}">'.format(content),
            )
            self.assertEqual(
                og_prop(content, "http://some/{}".format(content)),
                '<meta property="og:{0}" content="http://some/{0}">'.format(content),
            )
        self.assertEqual(
            og_prop("random_type", "https://some/random_type"),
            '<meta property="og:random_type" content="https://some/random_type">',
        )
        self.assertEqual(
            og_prop("random_type", "http://some/random_type"),
            '<meta property="og:random_type" content="http://some/random_type">',
        )

    def test_og_full_media_data(self):
        media = {
            "url": "https://some/media.url",
            "secure_url": "https://some/media.url",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        for content in ("image", "video", "audio"):
            self.assertEqual(
                og_prop(content, media),
                '<meta property="og:{0}:alt" content="a media">\n'
                '<meta property="og:{0}:height" content="100">\n'
                '<meta property="og:{0}:secure_url" content="https://some/media.url">\n'
                '<meta property="og:{0}:type" content="some/mime">\n'
                '<meta property="og:{0}:url" content="https://some/media.url">\n'
                '<meta property="og:{0}:width" content="100">'
                "".format(content),
            )

    def test_generic_prop_basically_works(self):
        self.assertEqual(generic_prop("og", "type", "website"), '<meta property="og:type" content="website">')

    def test_generic_prop_escapes_xss(self):
        self.assertEqual(
            generic_prop("og", 't"y&p<e', "web&site"),
            '<meta property="og:t&quot;y&amp;p&lt;e" content="web&amp;site">',
        )


class MetaTestCase(TestCase):
    def test_meta_basically_works(self):
        self.assertEqual(
            meta("description", "Awesome website about ponies"),
            '<meta name="description" content="Awesome website about ponies">',
        )

    def test_meta_escapes_xss(self):
        self.assertEqual(
            meta('desc"rip&tion', "Awesome website < about ponies"),
            '<meta name="desc&quot;rip&amp;tion" content="Awesome website &lt; about ponies">',
        )


class CustomMetaTestCase(TestCase):
    def test_custom_meta_basically_works(self):
        self.assertEqual(custom_meta("property", "foo", "bar"), '<meta property="foo" content="bar">')

    def test_custom_meta_escapes_xss(self):
        self.assertEqual(
            custom_meta("prop&erty", 'fo"o', "b<ar"), '<meta prop&amp;erty="fo&quot;o" content="b&lt;ar">'
        )


class TwitterPropTestCase(TestCase):
    def test_twitter_basically_works(self):
        self.assertEqual(twitter_prop("foo", "bar"), '<meta name="twitter:foo" content="bar">')

    def test_twitter_escapes_xss(self):
        self.assertEqual(twitter_prop('fo"o', "b<ar"), '<meta name="twitter:fo&quot;o" content="b&lt;ar">')


class FacebookPropTestCase(TestCase):
    def test_facebook_basically_works(self):
        self.assertEqual(facebook_prop("foo", "bar"), '<meta property="fb:foo" content="bar">')


class GooglePlusPropTestcase(TestCase):
    def setUp(self):
        # The __warningregistry__'s need to be in a pristine state for tests
        # to work properly.
        for v in sys.modules.values():
            if getattr(v, "__warningregistry__", None):
                v.__warningregistry__ = {}

    def test_google_plus_basically_works(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(googleplus_prop("foo", "bar"), '<meta itemprop="foo" content="bar">')
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    def test_google_plus_html_scope_works(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(googleplus_html_scope("bar"), ' itemscope itemtype="https://schema.org/bar" ')
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    def test_google_plus_scope_works(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(googleplus_scope("bar"), ' itemscope itemtype="https://schema.org/bar" ')
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    def test_google_plus_escapes_xss(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(googleplus_prop('fo"o', "b<ar"), '<meta itemprop="fo&quot;o" content="b&lt;ar">')
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    def test_meta_namespaces_gplus(self):
        context_use_schemaorg = {"meta": Meta(use_schemaorg=True)}
        context_no_use_schemaorg = {"meta": Meta(use_schemaorg=False)}

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(meta_namespaces_gplus({}), "")
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(meta_namespaces_gplus(context_no_use_schemaorg), "")
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.assertEqual(
                meta_namespaces_gplus(context_use_schemaorg), ' itemscope itemtype="https://schema.org/Article" '
            )
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)


class SchemaOrgPropTestcase(TestCase):
    def test_schemaorg_basically_works(self):
        self.assertEqual(schemaorg_prop("foo", "bar"), '<meta itemprop="foo" content="bar">')

    def test_schemaorg_html_scope_works(self):
        self.assertEqual(schemaorg_html_scope("bar"), ' itemscope itemtype="https://schema.org/bar" ')

    def test_schemaorg_scope_works(self):
        self.assertEqual(schemaorg_scope("bar"), ' itemscope itemtype="https://schema.org/bar" ')

    def test_schemaorg_escapes_xss(self):
        self.assertEqual(schemaorg_prop('fo"o', "b<ar"), '<meta itemprop="fo&quot;o" content="b&lt;ar">')

    def test_meta_namespaces_gplus(self):
        context_use_schemaorg = {"meta": Meta(use_schemaorg=True)}
        context_no_use_schemaorg = {"meta": Meta(use_schemaorg=False)}

        self.assertEqual(meta_namespaces_schemaorg({}), "")

        self.assertEqual(meta_namespaces_schemaorg(context_no_use_schemaorg), "")

        self.assertEqual(
            meta_namespaces_schemaorg(context_use_schemaorg), ' itemscope itemtype="https://schema.org/Article" '
        )


class MetaListTestCase(TestCase):
    def test_meta_list_basically_works(self):
        self.assertEqual(
            meta_list("keywords", ["foo", "bar", "baz"]), '<meta name="keywords" content="foo, bar, baz">'
        )

    def test_meta_list_with_non_list_value(self):
        self.assertEqual(meta_list("keywords", 12), "")

    def test_meta_list_escapes_xss(self):
        self.assertEqual(
            meta_list("keywords", ['fo"o', "bar", "b<az"]), '<meta name="keywords" content="fo&quot;o, bar, b&lt;az">'
        )


class MetaExtrasTestCase(TestCase):
    def test_meta_extras_basically_works(self):
        result = meta_extras(None)
        self.assertEqual(result, "")
        result = meta_extras({"type": "foo", "image_width": "bar"})
        self.assertTrue('<meta name="type" content="foo">' in result)
        self.assertTrue('<meta name="image_width" content="bar">' in result)


class CustomMetaExtrasTestCase(TestCase):
    def test_custom_meta_extras_basically_works(self):
        result = custom_meta_extras(None)
        self.assertEqual(result, "")
        result = custom_meta_extras([("property", "type", "foo"), ("key", "image_width", "bar")])
        self.assertTrue('<meta property="type" content="foo">' in result)
        self.assertTrue('<meta key="image_width" content="bar">' in result)


class MetaNamespaceTestCase(TestCase):
    def test_meta_namespaces_no_meta_in_context(self):
        context = {}
        result = meta_namespaces(context)
        expected = ""
        self.assertEqual(result, expected)

    def test_meta_namespaces_default(self):
        context = {"meta": Meta()}
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_facebook(self):
        context = {"meta": Meta(use_facebook=True)}
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_custom(self):
        context = {"meta": Meta(custom_namespace="my-website")}
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# my-website: http://ogp.me/ns/my-website#"'
        self.assertEqual(result, expected)

    def test_meta_namespaces_facebook_and_custom(self):
        context = {"meta": Meta(use_facebook=True, custom_namespace="my-website")}
        result = meta_namespaces(context)
        expected = ' prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# my-website: http://ogp.me/ns/my-website#"'
        self.assertEqual(result, expected)


class TitlePropTestCase(TestCase):
    def test_title_prop_basically_works(self):
        self.assertEqual(title_prop("I love django-meta app!"), "<title>I love django-meta app!</title>")

    def test_title_prop_escapes_xss(self):
        self.assertEqual(
            title_prop('I love "django-meta" app! >&:-)'),
            "<title>I love &quot;django-meta&quot; app! &gt;&amp;:-)</title>",
        )
