import warnings
from copy import copy

from django.test import TestCase

from meta import settings
from meta.views import Meta, MetadataMixin


class MetadataMixinTestCase(TestCase):
    def test_get_meta_class(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_class(), Meta)

    def test_get_meta_title(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_title(), None)

        m.title = "Foo"
        self.assertEqual(m.get_meta_title(), "Foo")

    def test_get_meta_og_title(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_og_title(), None)

        m.og_title = "Foo"
        self.assertEqual(m.get_meta_og_title(), "Foo")

    def test_get_meta_twitter_title(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_twitter_title(), None)

        m.twitter_title = "Foo"
        self.assertEqual(m.get_meta_twitter_title(), "Foo")

    def test_get_meta_schemaorg_title(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_schemaorg_title(), None)

        m.schemaorg_title = "Foo"
        self.assertEqual(m.get_meta_schemaorg_title(), "Foo")

    def test_get_meta_description(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_description(), None)

        m.description = "Foo"
        self.assertEqual(m.get_meta_description(), "Foo")

    def test_get_meta_url(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_url(), None)

        m.url = "/foo/bar"
        self.assertEqual(m.get_meta_url(), "/foo/bar")

    def test_get_meta_image(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_image(), None)

        m.image = "img/foo.gif"

        self.assertEqual(m.get_meta_image(), "img/foo.gif")

    def test_get_meta_image_object(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_image(), None)
        media = {
            "url": "http://meta.example.com/image.gif",
            "secure_url": "https://meta.example.com/custom.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        m.image_object = media

        self.assertEqual(m.get_meta_image_object(), media)
        self.assertEqual(m.get_meta_image(), media["url"])

    def test_get_meta_object_tye(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_object_type(), None)

        m.object_type = "bar"
        self.assertEqual(m.get_meta_object_type(), "bar")

    def test_get_domain(self):
        domain = settings.SITE_DOMAIN
        settings.SITE_DOMAIN = "somedomain.com"
        m = MetadataMixin()
        self.assertEqual(m.get_domain(), "somedomain.com")
        settings.SITE_DOMAIN = domain

    def test_get_domain_http(self):
        protocol = settings.SITE_PROTOCOL
        settings.SITE_PROTOCOL = "http"
        m = MetadataMixin()
        self.assertEqual(m.get_protocol(), "http")
        settings.SITE_PROTOCOL = protocol

    def test_get_meta_object_type_with_setting(self):
        m = MetadataMixin()

        settings.SITE_TYPE = "foo"

        self.assertEqual(m.get_meta_object_type(), "foo")

    def test_get_meta_site_name(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_site_name(), None)

        m.site_name = "Foo"
        self.assertEqual(m.get_meta_site_name(), "Foo")

    def test_get_meta_site_name_with_setting(self):
        m = MetadataMixin()

        settings.SITE_NAME = "Foo"

        self.assertEqual(m.get_meta_site_name(), "Foo")

    def test_get_meta_extra_props(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_extra_props(), None)

        m.extra_props = {"app_name": "Foo", "app_id": "Bar"}
        self.assertEqual(m.get_meta_extra_props(), {"app_name": "Foo", "app_id": "Bar"})

    def test_get_meta_extra_custom_props(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_extra_custom_props(), None)

        m.extra_custom_props = [
            ("property", "app_name", "Foo"),
            ("property", "app_id", "Bar"),
        ]
        self.assertEqual(
            m.get_meta_extra_custom_props(), [("property", "app_name", "Foo"), ("property", "app_id", "Bar")]
        )

    def test_get_meta_custom_namespace(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_custom_namespace(), None)

        m.custom_namespace = "my-website"
        self.assertEqual(m.get_meta_custom_namespace(), "my-website")

        settings.OG_NAMESPACES = ["foo", "bar"]
        m = MetadataMixin()
        self.assertEqual(m.get_meta_custom_namespace(), ["foo", "bar"])
        settings.OG_NAMESPACES = None

    def test_get_meta_twitter_site(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_twitter_site(), None)

        m.twitter_site = "@foo"
        self.assertEqual(m.get_meta_twitter_site(), "@foo")

    def test_get_meta_twitter_creator(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_twitter_creator(), None)

        m.twitter_creator = "@foo"
        self.assertEqual(m.get_meta_twitter_creator(), "@foo")

    def test_get_meta_twitter_card(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            m = MetadataMixin()
            self.assertEqual(m.get_meta_twitter_card(), None)
            assert len(w) == 1
            assert issubclass(w[-1].category, PendingDeprecationWarning)

            m.twitter_card = "summary"
            assert len(w) == 2
            assert issubclass(w[-1].category, PendingDeprecationWarning)

            self.assertEqual(m.twitter_card, "summary")
            assert len(w) == 3
            assert issubclass(w[-1].category, PendingDeprecationWarning)

            self.assertEqual(m.get_meta_twitter_card(), "summary")
            assert len(w) == 4
            assert issubclass(w[-1].category, PendingDeprecationWarning)

    def test_get_meta_twitter_type(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            m = MetadataMixin()
            self.assertEqual(m.get_meta_twitter_type(), None)
            assert len(w) == 0

            m.twitter_type = "summary"
            self.assertEqual(m.get_meta_twitter_type(), "summary")
            assert len(w) == 0

    def test_get_meta_facebook_app_id(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_facebook_app_id(), None)

        m.facebook_app_id = "12345"
        self.assertEqual(m.get_meta_facebook_app_id(), "12345")

    def test_get_meta_locale(self):
        m = MetadataMixin()
        self.assertEqual(m.get_meta_locale(), None)

        m.locale = "en_US"
        self.assertEqual(m.get_meta_locale(), "en_US")

    def test_get_meta(self):
        settings.SITE_PROTOCOL = "http"
        settings.SITE_DOMAIN = "foo.com"
        settings.USE_SITES = False
        settings.FB_PAGES = "fbpages"
        settings.FB_APPID = "appid"

        media = {
            "url": "images/foo.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        full_url_media = copy(media)
        full_url_media["url"] = "http://foo.com/static/images/foo.gif"
        m = MetadataMixin()
        m.title = "title"
        m.description = "description"
        m.keywords = ["foo", "bar"]
        m.url = "some/path"
        m.image_object = media

        meta_object = m.get_meta()

        self.assertTrue(type(meta_object), Meta)
        self.assertEqual(meta_object.title, "title")
        self.assertEqual(meta_object.description, "description")
        self.assertEqual(meta_object.url, "http://foo.com/some/path")
        self.assertEqual(meta_object.keywords, ["foo", "bar"])
        self.assertEqual(meta_object.image, "http://foo.com/static/images/foo.gif")
        self.assertEqual(meta_object.image_object, media)
        settings.SITE_DOMAIN = "example.com"

    def test_get_context(self):
        media = {
            "url": "images/foo.gif",
            "type": "some/mime",
            "width": 100,
            "height": 100,
            "alt": "a media",
        }
        full_url_media = copy(media)
        full_url_media["url"] = "https://foo.com/static/images/foo.gif"
        full_url_media["secure_url"] = "https://foo.com/static/images/foo.gif"

        class Super:
            def get_context_data(self):
                return {}

        class View(MetadataMixin, Super):
            title = "title"
            description = "description"
            keywords = ["foo", "bar"]
            url = "some/path"
            image_object = media

        settings.SITE_PROTOCOL = "https"
        settings.SITE_DOMAIN = "foo.com"
        settings.USE_SITES = False

        v = View()

        context = v.get_context_data()

        self.assertTrue("meta" in context)
        self.assertTrue(type(context["meta"]), Meta)
        self.assertEqual(context["meta"].url, "https://foo.com/some/path")
        self.assertEqual(context["meta"].keywords, ["foo", "bar"])
        self.assertEqual(context["meta"].image, "https://foo.com/static/images/foo.gif")
        self.assertEqual(context["meta"].image_object, full_url_media)

        settings.SITE_PROTOCOL = "http"
        settings.SITE_DOMAIN = "example.com"
        settings.FB_PAGES = ""
        settings.FB_APPID = ""
