import warnings
from datetime import timedelta

from app_helper.base_test import BaseTestCase
from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings
from django.utils import timezone

from meta.models import ModelMeta
from meta.settings import get_setting
from meta.templatetags.meta_extra import generic_prop, googleplus_html_scope

from .example_app.models import Comment, Post, Publisher


class TestMeta(BaseTestCase):
    post = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.publisher, __ = Publisher.objects.get_or_create(name="publisher name")
        cls.post, __ = Post.objects.get_or_create(
            title="a title",
            og_title="og title",
            twitter_title="twitter title",
            schemaorg_title="schemaorg title",
            schemaorg_description="schemaorg description",
            slug="title",
            abstract="post abstract",
            meta_description="post meta",
            meta_keywords="post keyword1,post keyword 2",
            author=cls.user,
            date_published_end=timezone.now() + timedelta(days=2),
            text="post text",
            image_url="/path/to/image",
            publisher=cls.publisher,
        )
        cls.related_post, __ = Post.objects.get_or_create(
            title="related title",
            og_title="related og title",
            twitter_title="related twitter title",
            schemaorg_title="related schemaorg title",
            schemaorg_description="related schemaorg description",
            slug="related-title",
            abstract="related post abstract",
            meta_description="related post meta",
            meta_keywords="related post keyword1,related post keyword 2",
            author=cls.user,
            date_published_end=timezone.now() + timedelta(days=2),
            text="related post text",
            image_url="/path/to/related-image",
        )
        cls.comment, __ = Comment.objects.get_or_create(
            body="comment body",
            post=cls.post,
        )
        cls.post.related_posts.add(cls.related_post)
        cls.post.main_image, __ = cls.create_django_image()
        cls.post.save()
        cls.related_post.main_image, __ = cls.create_django_image()
        cls.related_post.save()
        cls.image_url = cls.post.main_image.url
        cls.related_image_url = cls.related_post.main_image.url
        cls.image_width = cls.post.main_image.width
        cls.image_height = cls.post.main_image.height

    @override_settings(META_SITE_PROTOCOL="http", META_USE_SITES=True)
    def test_as_meta(self):
        expected = {
            "locale": "dummy_locale",
            "image": "http://example.com{}".format(self.image_url),
            "image_width": self.image_width,
            "image_height": self.image_height,
            "object_type": "Article",
            "tag": None,
            "keywords": ["post keyword1", "post keyword 2"],
            "og_profile_id": "1111111111111",
            "twitter_description": "post meta",
            "schemaorg_type": "Article",
            "title": "a title",
            "og_title": "og title",
            "twitter_title": "twitter title",
            "schemaorg_title": "schemaorg title",
            "schemaorg_description": "schemaorg description",
            "expiration_time": self.post.date_published_end,
            "og_description": "post meta",
            "description": "post meta",
            "twitter_type": "Summary",
            "modified_time": self.post.date_modified,
            "og_author_url": "https://facebook.com/foo.bar",
            "og_app_id": "appid",
            "fb_pages": "fbpages",
            "published_time": self.post.date_published,
            "url": "http://example.com/title/",
            "og_publisher": "https://facebook.com/foo.blag",
            "og_type": "Article",
            "twitter_author": "@FooBar",
            "twitter_site": "@FooBlag",
            "false_prop": False,
            "other_prop": "get_other_prop",
            "custom_namespace": ["foo", "bar"],
            "extra_props": {"key": "val"},
            "extra_custom_props": [
                ("custom1", "custom_name1", "custom_val1"),
                ("custom2", "custom_name2", "custom_val2"),
            ],
            "schema": {
                "@type": "Article",
                "image": "http://example.com{}".format(self.image_url),
                "articleBody": "post text",
                "articleSection": ["category 1", "category 2"],
                "author": {
                    "@type": "Person",
                    "name": self.post.author.get_full_name(),
                },
                "copyrightYear": self.post.date_published.year,
                "dateCreated": self.post.date_created.isoformat(),
                "dateModified": self.post.date_modified.isoformat(),
                "datePublished": self.post.date_published.isoformat(),
                "expires": self.post.date_published_end.isoformat(),
                "headline": "post abstract",
                "keywords": ["post keyword1", "post keyword 2"],
                "description": "post meta",
                "name": "a title",
                "url": "http://example.com/title/",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": "http://example.com/title/",
                },
                "publisher": {
                    "@type": "Organization",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "http://example.com/some/logo.png",
                    },
                    "name": "publisher name",
                },
                "comment": [{"@type": "Comment", "text": "comment body"}],
                "commentCount": self.post.comments.count(),
                "citation": [
                    {
                        "@type": "Article",
                        "articleBody": "related post text",
                        "articleSection": ["category 1", "category 2"],
                        "author": {"@type": "Person", "name": self.related_post.author.get_full_name()},
                        "citation": [],
                        "comment": [],
                        "commentCount": self.related_post.comments.count(),
                        "copyrightYear": self.related_post.date_published.year,
                        "dateCreated": self.related_post.date_created.isoformat(),
                        "dateModified": self.related_post.date_modified.isoformat(),
                        "datePublished": self.related_post.date_published.isoformat(),
                        "description": "related post meta",
                        "expires": self.related_post.date_published_end.isoformat(),
                        "headline": "related post abstract",
                        "image": "http://example.com{}".format(self.related_image_url),
                        "keywords": ["related post keyword1", "related post keyword 2"],
                        "mainEntityOfPage": {"@id": "http://example.com/related-title/", "@type": "WebPage"},
                        "name": "related title",
                        "publisher": None,
                        "url": "http://example.com/related-title/",
                    }
                ],
            },
        }
        with override_settings(META_OG_NAMESPACES=["foo", "bar"], META_FB_PAGES="fbpages", META_FB_APPID="appid"):
            meta = self.post.as_meta()
            self.assertTrue(meta)
            for key in expected.keys():
                value = expected[key]
                if value is not None:
                    self.assertEqual(value, getattr(meta, key))
                else:
                    self.assertFalse(hasattr(meta, key))

            self.assertEqual(self.post.build_absolute_uri("hi"), "http://example.com/hi")
            self.assertEqual(self.post.build_absolute_uri("http://example.com/hi"), "http://example.com/hi")

    @override_settings(META_SITE_PROTOCOL="http", META_FB_PAGES="fbpages", META_FB_APPID="appid")
    def test_as_meta_with_request(self):
        # Server is different as it's taken directly from the request object
        media = {
            "url": "https://testserver{}".format(self.image_url),
            "width": self.image_width,
            "height": self.image_height,
            "alt": "a title",
        }
        expected = {
            "locale": "dummy_locale",
            "image_object": media,
            "image": "https://testserver{}".format(self.image_url),
            "image_width": self.image_width,
            "image_height": self.image_height,
            "object_type": "Article",
            "tag": False,
            "keywords": ["post keyword1", "post keyword 2"],
            "og_profile_id": "1111111111111",
            "twitter_description": "post meta",
            "schemaorg_type": "Article",
            "title": "a title",
            "og_title": "og title",
            "twitter_title": "twitter title",
            "schemaorg_title": "schemaorg title",
            "schemaorg_description": "schemaorg description",
            "expiration_time": self.post.date_published_end,
            "og_description": "post meta",
            "description": "post meta",
            "twitter_type": "Summary",
            "modified_time": self.post.date_modified,
            "og_author_url": "https://facebook.com/foo.bar",
            "og_app_id": "appid",
            "fb_pages": "fbpages",
            "published_time": self.post.date_published,
            "url": "https://testserver/title/",
            "og_publisher": "https://facebook.com/foo.blag",
            "og_type": "Article",
            "twitter_author": "@FooBar",
            "twitter_site": "@FooBlag",
            "custom_namespace": None,
            "extra_props": {"key": "val"},
            "extra_custom_props": [
                ("custom1", "custom_name1", "custom_val1"),
                ("custom2", "custom_name2", "custom_val2"),
            ],
            "schema": {
                "@type": "Article",
                "image": "http://example.com{}".format(self.image_url),
                "articleBody": "post text",
                "articleSection": ["category 1", "category 2"],
                "author": {
                    "@type": "Person",
                    "name": self.post.author.get_full_name(),
                },
                "copyrightYear": self.post.date_published.year,
                "dateCreated": self.post.date_created.isoformat(),
                "dateModified": self.post.date_modified.isoformat(),
                "datePublished": self.post.date_published.isoformat(),
                "expires": self.post.date_published_end.isoformat(),
                "headline": "post abstract",
                "keywords": ["post keyword1", "post keyword 2"],
                "description": "post meta",
                "name": "a title",
                "url": "http://example.com/title/",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": "http://example.com/title/",
                },
                "publisher": {
                    "@type": "Organization",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "http://example.com/some/logo.png",
                    },
                    "name": "publisher name",
                },
                "comment": [{"@type": "Comment", "text": "comment body"}],
                "commentCount": self.post.comments.count(),
                "citation": [
                    {
                        "@type": "Article",
                        "articleBody": "related post text",
                        "articleSection": ["category 1", "category 2"],
                        "author": {"@type": "Person", "name": self.related_post.author.get_full_name()},
                        "citation": [],
                        "comment": [],
                        "commentCount": self.related_post.comments.count(),
                        "copyrightYear": self.related_post.date_published.year,
                        "dateCreated": self.related_post.date_created.isoformat(),
                        "dateModified": self.related_post.date_modified.isoformat(),
                        "datePublished": self.related_post.date_published.isoformat(),
                        "description": "related post meta",
                        "expires": self.related_post.date_published_end.isoformat(),
                        "headline": "related post abstract",
                        "image": "http://example.com{}".format(self.related_image_url),
                        "keywords": ["related post keyword1", "related post keyword 2"],
                        "mainEntityOfPage": {"@id": "http://example.com/related-title/", "@type": "WebPage"},
                        "name": "related title",
                        "publisher": None,
                        "url": "http://example.com/related-title/",
                    }
                ],
            },
        }
        request = self.get_request(None, "en", path="/title/", secure=True)
        meta = self.post.as_meta(request)
        self.assertTrue(meta)
        for key in ModelMeta._metadata_default.keys():
            value = expected[key]
            if value is not False:
                self.assertEqual(value, getattr(meta, key))
            else:
                self.assertFalse(hasattr(meta, key))

    @override_settings(META_SITE_PROTOCOL="http")
    def test_as_meta_get_request_deprecation(self):
        request = self.get_request(None, "en", path="/title/", secure=True)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.post.get_meta(request)
            assert len(w) == 0

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.post.get_request()
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    @override_settings(
        META_USE_SITES=True,
        META_SITE_PROTOCOL="http",
        META_USE_OG_PROPERTIES=True,
        META_USE_TWITTER_PROPERTIES=True,
        META_USE_SCHEMAORG_PROPERTIES=True,
        META_USE_JSON_LD_SCHEMA=True,
    )
    def test_templatetag(self):
        self.post.as_meta()
        response = self.client.get("/title/")
        self.assertContains(response, '<html  itemscope itemtype="https://schema.org/Article" >')
        self.assertNotContains(response, '    itemscope itemtype="https://schema.org/Article"')
        self.assertContains(response, 'article:published_time"')
        self.assertContains(
            response, '<meta name="twitter:image" content="http://example.com{}">'.format(self.image_url)
        )
        self.assertContains(
            response, '<meta itemprop="description" content="{}">'.format(self.post.schemaorg_description)
        )
        self.assertContains(
            response, '<meta name="twitter:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(
            response, '<meta property="og:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(response, '<meta name="description" content="{}">'.format(self.post.meta_description))
        self.assertContains(
            response, '<meta name="keywords" content="{}">'.format(", ".join(self.post.meta_keywords.split(",")))
        )
        self.assertContains(response, '<meta name="key" content="val">')
        self.assertContains(response, '<meta custom1="custom_name1" content="custom_val1">')
        self.assertContains(response, '<meta custom2="custom_name2" content="custom_val2">')
        self.assertContains(response, '<meta property="og:{}:alt" content="a title">'.format("image"))
        self.assertContains(response, '<meta property="og:{}:height" content="{}">'.format("image", self.image_height))
        self.assertContains(response, '<meta property="og:{}:width" content="{}">'.format("image", self.image_width))
        self.assertContains(
            response,
            '<meta property="og:{}:url" content="{}'.format("image", "http://example.com{}".format(self.image_url)),
        )
        print(response.content)
        self.assertContains(
            response, '<script type="application/ld+json">{}</script>'.format(self.post.as_meta().as_json_ld())
        )

    @override_settings(
        META_SITE_PROTOCOL="http",
        META_USE_SITES=True,
        META_USE_OG_PROPERTIES=True,
        META_USE_TWITTER_PROPERTIES=True,
        META_USE_SCHEMAORG_PROPERTIES=True,
    )
    def test_templatetag_metadatamixin(self):
        """
        Test for issue #11
        """
        response = self.client.get("/mixin/title/")
        self.assertContains(response, '<meta itemprop="description" content="{}">'.format(self.post.meta_description))
        self.assertContains(
            response, '<meta name="twitter:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(
            response, '<meta property="og:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(response, '<meta name="description" content="{}">'.format(self.post.meta_description))
        self.assertContains(
            response, '<meta name="keywords" content="{}">'.format(", ".join(self.post.meta_keywords.split(",")))
        )
        self.assertContains(response, '<meta name="twitter:image" content="http://example.com/path/to/image">')

    @override_settings(
        META_USE_SITES=True,
        META_SITE_PROTOCOL="http",
        META_USE_OG_PROPERTIES=True,
        META_USE_TWITTER_PROPERTIES=True,
        META_USE_SCHEMAORG_PROPERTIES=True,
    )
    def test_templatetag_metadatamixin_image_object(self):
        """
        Test for issue #11
        """
        response = self.client.get("/mixin_image/title/")
        self.assertContains(response, '<meta itemprop="description" content="{}">'.format(self.post.meta_description))
        self.assertContains(
            response, '<meta name="twitter:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(
            response, '<meta property="og:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(response, '<meta name="description" content="{}">'.format(self.post.meta_description))
        self.assertContains(
            response, '<meta name="keywords" content="{}">'.format(", ".join(self.post.meta_keywords.split(",")))
        )
        self.assertContains(
            response, '<meta name="twitter:image" content="http://example.com{}">'.format(self.image_url)
        )
        self.assertContains(response, '<meta property="og:{}:alt" content="a title">'.format("image"))
        self.assertContains(response, '<meta property="og:{}:height" content="{}">'.format("image", self.image_height))
        self.assertContains(response, '<meta property="og:{}:width" content="{}">'.format("image", self.image_width))
        self.assertContains(
            response,
            '<meta property="og:{}:url" content="{}'.format("image", "http://example.com{}".format(self.image_url)),
        )

    @override_settings(META_SITE_DOMAIN="example.com", META_USE_OG_PROPERTIES=True)
    def test_templatetag_secure_image(self):
        """
        Test for issue #79
        """
        with override_settings(META_SITE_PROTOCOL="http"):
            response = self.client.get("/mixin/title/")
            self.assertContains(response, '<meta property="og:image" content="http://example.com/path/to/image">')
        with override_settings(META_SITE_PROTOCOL="https"):
            response = self.client.get("/mixin/title/")
            self.assertContains(response, '<meta property="og:image" content="https://example.com/path/to/image">')
            self.assertContains(
                response, '<meta property="og:image:secure_url" content="https://example.com/path/to/image">'
            )

    @override_settings(
        META_USE_SITES=True,
        META_USE_OG_PROPERTIES=False,
        META_USE_TWITTER_PROPERTIES=True,
        META_SITE_PROTOCOL="http",
        META_USE_SCHEMAORG_PROPERTIES=True,
    )
    def test_templatetag_no_og(self):
        response = self.client.get("/title/")
        self.assertFalse(response.rendered_content.find("og:description") > -1)
        self.assertContains(
            response, '<meta itemprop="description" content="{}">'.format(self.post.schemaorg_description)
        )
        self.assertContains(
            response, '<meta name="twitter:description" content="{}">'.format(self.post.meta_description)
        )
        self.assertContains(
            response, '<meta name="keywords" content="{}">'.format(", ".join(self.post.meta_keywords.split(",")))
        )

    @override_settings(META_OG_NAMESPACES=["foo", "bar"], META_USE_SITES=True, META_SITE_PROTOCOL="http")
    def test_templatetag_custom_namespaces(self):
        response = self.client.get("/title/")
        for ns in get_setting("OG_NAMESPACES"):
            self.assertContains(response, "{0}: http://ogp.me/ns/{0}#".format(ns))

    def test_generic_prop_basically_works(self):
        """
        Test vendorized generic_prop templatetag
        """
        self.assertEqual(generic_prop("og", "type", "website"), '<meta property="og:type" content="website">')

    def test_google_plus_scope_works(self):
        """
        Test vendorized googleplus_scope templatetag
        """
        self.assertEqual(googleplus_html_scope("bar"), ' itemscope itemtype="https://schema.org/bar" ')

    @override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="https")
    def test_image_protocol_https(self):
        meta = self.post.as_meta()
        self.assertEqual("https://example.com{}".format(self.image_url), meta.image)

    @override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="http")
    def test_image_protocol_http(self):
        meta = self.post.as_meta()
        self.assertEqual("http://example.com{}".format(self.image_url), meta.image)

    def test_not_use_sites(self):
        with override_settings(META_USE_SITES=False):
            with self.assertRaises(RuntimeError):
                self.post.as_meta()
        with override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="http"):
            meta = self.post.as_meta()
            self.assertEqual(meta.url, "http://example.com/title/")

    @override_settings(META_SITE_PROTOCOL=None)
    def test_get_meta_protocol_without_site_protocol_will_raise(self):
        with self.assertRaises(ImproperlyConfigured):
            self.post.get_meta_protocol()

    def test_get_meta_protocol(self):
        with override_settings(META_SITE_PROTOCOL="http"):
            self.assertEqual(self.post.get_meta_protocol(), "http")
        with override_settings(META_SITE_PROTOCOL="https"):
            self.assertEqual(self.post.get_meta_protocol(), "https")

    def test_get_author_schemaorg(self):
        self.assertEqual(self.post.get_author_schemaorg(), "https://schemaorg-profile.com")
