from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from meta.models import ModelMeta
from meta.views import Meta

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class Publisher(ModelMeta, models.Model):
    name = models.CharField(_("name"), max_length=255)

    _schema = {
        "@type": "Organization",
        "name": "name",
        "logo": "static_logo",
    }

    class Meta:
        verbose_name = _("publisher")
        verbose_name_plural = _("publishers")

    def __str__(self):
        return self.name

    @property
    def static_logo(self):
        return Meta(schema={"@type": "ImageObject", "url": self.build_absolute_uri("/some/logo.png")})


class Comment(ModelMeta, models.Model):
    body = models.CharField(_("comment"), max_length=255)
    post = models.ForeignKey(
        "example_app.Post", on_delete=models.CASCADE, verbose_name=_("post"), related_name="comments"
    )

    _schema = {"@type": "Comment", "text": "body"}

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.body[:10]


class Post(ModelMeta, models.Model):
    """
    Blog post
    """

    title = models.CharField(_("Title"), max_length=255)
    og_title = models.CharField(_("Opengraph title"), blank=True, max_length=255)
    twitter_title = models.CharField(_("Twitter title"), blank=True, max_length=255)
    schemaorg_title = models.CharField(_("Schema.org title"), blank=True, max_length=255)
    schemaorg_description = models.CharField(_("Schema.org description"), blank=True, max_length=255)
    slug = models.SlugField(_("slug"))
    abstract = models.TextField(_("Abstract"))
    meta_description = models.TextField(verbose_name=_("Post meta description"), blank=True, default="")
    meta_keywords = models.TextField(verbose_name=_("Post meta keywords"), blank=True, default="")
    author = models.ForeignKey(User, verbose_name=_("Author"), null=True, blank=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(_("Published Since"), default=timezone.now)
    date_published_end = models.DateTimeField(_("Published Until"), null=True, blank=True)
    main_image = models.ImageField(verbose_name=_("Main image"), blank=True, upload_to="images", null=True)
    text = models.TextField(verbose_name=_("Post text"), blank=True, default="")
    image_url = models.CharField(max_length=200, null=True, blank=True)
    publisher = models.ForeignKey(
        "example_app.Publisher", on_delete=models.CASCADE, verbose_name=_("publisher"), related_name="posts", null=True
    )
    related_posts = models.ManyToManyField("example_app.Post", verbose_name=_("related posts"), blank=True)

    _metadata_default = ModelMeta._metadata_default.copy()  # purely for testing purposes
    _metadata_default["locale"] = "dummy_locale"

    _metadata = {
        "title": "title",
        "og_title": "og_title",
        "twitter_title": "twitter title",
        "schemaorg_title": "schemaorg title",
        "schemaorg_description": "schemaorg description",
        "description": "get_description",
        "og_description": "get_description",
        "keywords": "get_keywords",
        "image_object": "get_image_object",
        "image": "get_image_full_url",
        "image_width": "get_image_width",
        "image_height": "get_image_height",
        "object_type": "Article",
        "og_type": "Article",
        "og_profile_id": "1111111111111",
        "og_publisher": "https://facebook.com/foo.blag",
        "og_author_url": "get_author_url",
        "twitter_type": "Summary",
        "twitter_site": "@FooBlag",
        "twitter_author": "get_author_twitter",
        "schemaorg_type": "Article",
        "published_time": "get_date",
        "modified_time": "get_date",
        "expiration_time": "get_date",
        "url": "get_full_url",
        "author": "get_author_name",
        "other_prop": "get_other_prop",
        "false_prop": "get_false_prop",
        "extra_props": {"key": "val"},
        "extra_custom_props": "get_custom_props",
    }

    _schema = {
        "image": "get_image_full_url",
        "articleBody": "text",
        "articleSection": "get_categories",
        "author": "get_schema_author",
        "copyrightYear": "copyright_year",
        "dateCreated": "get_date",
        "dateModified": "get_date",
        "datePublished": "get_date",
        "expires": "get_date",
        "headline": "headline",
        "keywords": "get_keywords",
        "description": "get_description",
        "name": "title",
        "url": "get_full_url",
        "mainEntityOfPage": "mainEntityOfPage",
        "publisher": "publisher",
        "comment": "comments",
        "commentCount": "comments_count",
        "citation": "related_posts",
    }

    class Meta:
        verbose_name = _("blog article")
        verbose_name_plural = _("blog articles")
        ordering = ("-date_published", "-date_created")
        get_latest_by = "date_published"

    def __str__(self):
        return self.title

    def get_date(self, param):
        if param in ("published_time", "datePublished"):
            return self.date_published
        elif param in ("modified_time", "dateModified"):
            return self.date_modified
        elif param in ("expiration_time", "expires"):
            return self.date_published_end
        elif param == "dateCreated":
            return self.date_created

    @property
    def copyright_year(self):
        return self.date_published.year

    @property
    def headline(self):
        return self.abstract[:110]

    @property
    def comments_count(self):
        return self.comments.count()

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_description
        if not description:
            description = self.abstract
        return description.strip()

    def get_image_object(self):
        if self.main_image:
            return {
                "url": self.build_absolute_uri(self.main_image.url),
                "width": self.main_image.width,
                "height": self.main_image.height,
                "alt": self.title,
            }

    def get_image_full_url(self):
        if self.main_image:
            return self.build_absolute_uri(self.main_image.url)

    def get_image_width(self):
        if self.main_image:
            return self.main_image.width

    def get_image_height(self):
        if self.main_image:
            return self.main_image.height

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_author(self):
        author = super().get_author()
        author.fb_url = "https://facebook.com/foo.bar"
        author.twitter_profile = "@FooBar"
        author.get_full_name = self.author.get_full_name
        author.schemaorg_profile = "https://schemaorg-profile.com"
        return author

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})

    @property
    def get_false_prop(self):
        return False

    def get_custom_props(self):
        return [("custom1", "custom_name1", "custom_val1"), ("custom2", "custom_name2", "custom_val2")]

    def get_categories(self):
        return ["category 1", "category 2"]

    def get_schema_author(self):
        author = self.get_author()
        return {
            "@type": "Person",
            "name": author.get_full_name(),
        }
