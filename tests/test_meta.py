import json
from copy import copy

from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase, modify_settings, override_settings

from meta.views import Meta


@override_settings(
    META_SITE_PROTOCOL="",
    META_USE_SITES=False,
    META_USE_OG_PROPERTIES=False,
    META_USE_TWITTER_PROPERTIES=False,
    META_USE_SCHEMAORG_PROPERTIES=False,
    META_USE_JSON_LD_SCHEMA=False,
)
class MetaObjectTestCase(TestCase):
    def test_defaults(self):
        m = Meta()
        self.assertEqual(m.title, None)
        self.assertEqual(m.og_title, None)
        self.assertEqual(m.schemaorg_title, None)
        self.assertEqual(m.schemaorg_description, None)
        self.assertEqual(m.twitter_title, None)
        self.assertEqual(m.description, None)
        self.assertEqual(m.extra_props, None)
        self.assertEqual(m.extra_custom_props, None)
        self.assertEqual(m.custom_namespace, None)
        self.assertEqual(m.keywords, [])
        self.assertEqual(m.url, None)
        self.assertEqual(m.image, None)
        self.assertEqual(m.image_object, None)
        self.assertEqual(m.object_type, None)
        self.assertEqual(m.site_name, None)
        self.assertEqual(m.twitter_site, None)
        self.assertEqual(m.twitter_creator, None)
        self.assertEqual(m.locale, None)
        self.assertEqual(m.facebook_app_id, None)
        self.assertEqual(m.use_og, False)
        self.assertEqual(m.use_sites, False)
        self.assertEqual(m.use_twitter, False)
        self.assertEqual(m.use_facebook, False)
        self.assertEqual(m.use_schemaorg, False)
        self.assertEqual(m.use_json_ld, False)
        self.assertEqual(m.fb_pages, "")
        self.assertEqual(m.og_app_id, "")
        self.assertEqual(m.use_title_tag, False)
        self.assertEqual(m.schema, {"@type": m.schemaorg_type})

    def test_set_keywords(self):
        m = Meta(keywords=["foo", "bar"])
        self.assertEqual(m.keywords[0], "foo")
        self.assertEqual(m.keywords[1], "bar")

    @override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="http", SITE_ID=None)
    def test_set_image_request(self):
        factory = RequestFactory()
        request = factory.get("/")
        Site.objects.create(domain=request.get_host())
        m = Meta(
            request=request,
            title="A page title",
            image="/static/image.png",
        )
        self.assertEqual(m.image, "http://testserver/static/image.png")

    @override_settings(META_INCLUDE_KEYWORDS=["baz"])
    def test_set_keywords_with_include(self):
        m = Meta(keywords=["foo", "bar"])
        self.assertEqual(m.keywords[0], "foo")
        self.assertEqual(m.keywords[1], "bar")
        self.assertEqual(m.keywords[2], "baz")

    def test_set_keywords_no_duplicate(self):
        m = Meta(keywords=["foo", "foo", "foo"])
        self.assertEqual(m.keywords[0], "foo")
        self.assertEqual(len(m.keywords), 1)

    @override_settings(META_USE_JSON_LD_SCHEMA=True)
    def test_use_json_ld(self):
        m = Meta()
        self.assertEqual(m.use_json_ld, True)

    @override_settings(META_FB_APPID="appid", META_FB_PAGES="fbpages")
    def test_pages_appid(self):
        m = Meta()
        self.assertEqual(m.fb_pages, "fbpages")
        self.assertEqual(m.og_app_id, "appid")

    @override_settings(META_DEFAULT_KEYWORDS=["foo", "bar"])
    def test_set_keywords_with_defaults(self):
        m = Meta()
        self.assertEqual(m.keywords[0], "foo")
        self.assertEqual(m.keywords[1], "bar")

    @override_settings(META_OG_NAMESPACES=["foo", "bar"])
    def test_set_namespaces(self):
        m = Meta()
        self.assertEqual(m.custom_namespace[0], "foo")
        self.assertEqual(m.custom_namespace[1], "bar")

    def test_get_full_url_with_none(self):
        m = Meta()
        self.assertEqual(m.get_full_url(None), None)

    def test_get_full_url_with_full_url(self):
        m = Meta()
        self.assertEqual(m.get_full_url("http://example.com/foo"), "http://example.com/foo")

    def test_get_full_url_without_protocol_will_raise(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url("foo/bar")

    @override_settings(SITE_ID=None, META_USE_SITES=True, META_SITE_PROTOCOL="http")
    def test_get_full_url_without_site_id_will_raise(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url("foo/bar")

    @override_settings(SITE_ID=None, META_USE_SITES=True, META_SITE_PROTOCOL="http")
    def test_get_full_url_without_site_id_with_request_will_not_raise(self):
        factory = RequestFactory()
        request = factory.get("/")
        Site.objects.create(domain=request.get_host())
        m = Meta(request=request)
        self.assertEqual(m.get_full_url("foo/bar"), "http://testserver/foo/bar")

    @override_settings(SITE_ID=None, META_USE_SITES=True, META_SITE_PROTOCOL="http")
    def test_get_full_url_with_fdqn_original_url(self):
        factory = RequestFactory()
        request = factory.get("/")
        Site.objects.create(domain=request.get_host())
        m = Meta(request=request)
        self.assertEqual(m.get_full_url("https://example.com/foo/bar"), "https://example.com/foo/bar")

    def test_get_full_url_without_protocol_without_schema_will_raise(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url("//foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="http")
    def test_get_full_url_without_domain_will_raise(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            m.get_full_url("foo/bar")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_get_full_url_with_domain_and_protocol(self):
        m = Meta()
        self.assertEqual(m.get_full_url("foo/bar"), "https://foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_get_full_url_without_schema(self):
        m = Meta()
        self.assertEqual(m.get_full_url("//foo.com/foo/bar"), "https://foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_get_full_url_with_absolute_path(self):
        m = Meta()
        self.assertEqual(m.get_full_url("/foo/bar"), "https://foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="http", META_SITE_DOMAIN="http://foo.com")
    def test_get_full_url_with_wrong_domain(self):
        m = Meta()
        self.assertEqual(m.get_full_url("/foo/bar"), "http://foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_set_url(self):
        m = Meta(url="foo/bar")
        self.assertEqual(m.url, "https://foo.com/foo/bar")

    @override_settings(META_SITE_PROTOCOL="https")
    def test_set_image_object_with_full_url(self):
        media = {
            "url": "http://meta.example.com/image.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        secure_media = copy(media)
        secure_media["secure_url"] = "https://meta.example.com/image.gif"
        m = Meta(image_object=media)
        self.assertEqual(m.image, "http://meta.example.com/image.gif")
        self.assertEqual(m.image_object, secure_media)

    @override_settings(META_SITE_PROTOCOL="https")
    def test_set_image_object_with_custom_secure(self):
        media = {
            "url": "http://meta.example.com/image.gif",
            "secure_url": "https://meta.example.com/custom.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        m = Meta(image_object=media)
        self.assertEqual(m.image, "http://meta.example.com/image.gif")
        self.assertEqual(m.image_object, media)

    def test_set_image_with_full_url(self):
        m = Meta(image="http://meta.example.com/image.gif")
        self.assertEqual(m.image, "http://meta.example.com/image.gif")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_set_image_object_with_absolute_path(self):
        media = {
            "url": "/img/image.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        secure_media = copy(media)
        secure_media["secure_url"] = "https://foo.com/img/image.gif"
        secure_media["url"] = "https://foo.com/img/image.gif"
        m = Meta(image_object=media)
        self.assertEqual(m.image, "https://foo.com/img/image.gif")
        self.assertEqual(m.image_object, secure_media)

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_set_image_with_absolute_path(self):
        m = Meta(image="/img/image.gif")
        self.assertEqual(m.image, "https://foo.com/img/image.gif")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com")
    def test_set_image_with_relative_path(self):
        m = Meta(image="img/image.gif")
        self.assertEqual(m.image, "https://foo.com/static/img/image.gif")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com", META_IMAGE_URL="/thumb/")
    def test_set_image_with_image_url(self):
        m = Meta(image="img/image.gif")
        self.assertEqual(m.image, "https://foo.com/thumb/img/image.gif")

    @override_settings(
        META_SITE_PROTOCOL="https",
        META_SITE_DOMAIN="foo.com",
        META_IMAGE_URL="/thumb/",
        META_DEFAULT_IMAGE="img/image.gif",
    )
    def test_set_image_with_default_image_url(self):
        m = Meta()
        self.assertEqual(m.image, "https://foo.com/thumb/img/image.gif")

    @override_settings(META_SITE_PROTOCOL="https", META_SITE_DOMAIN="foo.com", META_DEFAULT_IMAGE="img/image.gif")
    def test_set_image_with_defaults(self):
        m = Meta()
        self.assertEqual(m.image, "https://foo.com/static/img/image.gif")

    def test_schema_org(self):
        m = Meta(schema={"foo": "bar", "list": [{"fuu": "baz", "test": "schema"}]})
        self.assertEqual(
            m.schema,
            {"foo": "bar", "list": [{"fuu": "baz", "test": "schema"}], "@type": m.schemaorg_type},
        )

    def test_as_json_ld(self):
        m = Meta(schema={"foo": "bar", "list": [{"fuu": "baz", "test": "schema"}]})
        data = m.schema
        data["@context"] = "http://schema.org"
        self.assertEqual(
            m.as_json_ld(),
            json.dumps(data),
        )

    @override_settings(META_SITE_DOMAIN="example-no-sites.com", META_SITE_PROTOCOL="http")
    @modify_settings(INSTALLED_APPS={"remove": "django.contrib.sites"})
    def test_get_full_url_without_sites(self):
        m = Meta()
        self.assertEqual(m.get_full_url("foo/bar"), "http://example-no-sites.com/foo/bar")

    @override_settings(
        META_SITE_DOMAIN="example-no-sites.com",
        META_SITE_PROTOCOL="http",
        META_USE_SITES=True,
    )
    @modify_settings(INSTALLED_APPS={"remove": "django.contrib.sites"})
    def test_get_full_url_without_sites_wrong_setting(self):
        m = Meta()
        with self.assertRaises(ImproperlyConfigured):
            self.assertEqual(m.get_full_url("foo/bar"), "http://example-no-sites.com/foo/bar")
