from __future__ import unicode_literals

from django.conf import settings as django_settings

from . import settings


class MetadataMixin(object):
    """ Django CBV mixin to prepare metadata for the view context """

    title = None
    description = None
    keywords = []
    url = None
    image = None
    object_type = None
    site_name = None
    use_og = settings.USE_OG_PROPERTIES

    def get_meta_title(self, context={}):
        return self.title

    def get_meta_description(self, context={}):
        return self.description

    def get_protocol(self):
        return settings.SITE_PROTOCOL

    def get_domain(self):
        return settings.SITE_DOMAIN

    def get_meta_url(self, url=None, context={}):
        url = url or self.url
        if not url:
            return None
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return '%s://%s%s' % (
                self.get_protocol(),
                self.get_domain(),
                url
            )
        return '%s://%s/%s' % (
            self.get_protocol(),
            self.get_domain(),
            url
        )

    def get_meta_image(self, image=None, context={}):
        image = image or self.image
        if not image:
            return None
        if image.startswith('/'):
            return self.get_meta_url(url=image, context=context)
        return self.get_meta_url(
            url='%s%s' % (django_settings.STATIC_URL, image),
            context=context
        )

    def get_meta_object_type(self, context={}):
        return self.object_type or settings.SITE_TYPE

    def get_meta_site_name(self, context={}):
        return self.site_name or settings.SITE_NAME

    def get_context_data(self, **kwargs):
        context = super(MetadataMixin, self).get_context_data(**kwargs)
        context['meta'] = {
            'use_og': self.use_og,
            'title': self.get_meta_title(context=context),
            'description': self.get_meta_description(context=context),
            'image': self.get_meta_image(context=context),
            'url': self.get_meta_url(context=context),
            'object_type': self.get_meta_object_type(context=context),
            'site_name': self.get_meta_site_name(context=context),
        }
        return context
