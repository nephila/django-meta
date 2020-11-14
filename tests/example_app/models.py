from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from meta.models import ModelMeta

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class Post(ModelMeta, models.Model):
    """
    Blog post
    """

    title = models.CharField(_("Title"), max_length=255)
    og_title = models.CharField(_("Opengraph title"), blank=True, max_length=255)
    twitter_title = models.CharField(_("Twitter title"), blank=True, max_length=255)
    schemaorg_title = models.CharField(_("Schema.org title"), blank=True, max_length=255)
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

    _metadata_default = ModelMeta._metadata_default.copy()  # purely for testing purposes
    _metadata_default["locale"] = "dummy_locale"

    _metadata = {
        "title": "title",
        "og_title": "og_title",
        "twitter_title": "twitter title",
        "schemaorg_title": "schemaorg title",
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
        "published_time": "date_published",
        "modified_time": "get_date",
        "expiration_time": "get_date",
        "url": "get_full_url",
        "author": "get_author_name",
        "other_prop": "get_other_prop",
        "false_prop": "get_false_prop",
        "extra_props": {"key": "val"},
        "extra_custom_props": "get_custom_props",
    }

    class Meta:
        verbose_name = _("blog article")
        verbose_name_plural = _("blog articles")
        ordering = ("-date_published", "-date_created")
        get_latest_by = "date_published"

    def get_date(self, param):
        if param == "published_time":
            return self.date_published
        elif param == "modified_time":
            return self.date_modified
        elif param == "expiration_time":
            return self.date_published_end

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
