from datetime import timedelta

from django.utils.lorem_ipsum import paragraphs, words
from django.utils.timezone import now
from django.views.generic import DetailView, ListView

from meta.views import Meta, MetadataMixin

from .models import Post

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = self.get_object().as_meta()
        return context


class PostMixinDetailView(MetadataMixin, DetailView):
    model = Post

    def get_meta_keywords(self, context):
        return self.object.meta_keywords.split(",")

    def get_meta_title(self, context):
        return self.object.title

    def get_meta_description(self, context):
        return self.object.meta_description

    def get_meta_image(self, context):
        return self.object.image_url

    def get_schema(self, context=None):
        url = reverse('post-detail-mixinx', kwargs={'slug': self.object.slug})
        return {
            'image': self.object.get_image_full_url(),
            'articleBody': self.object.text,
            'articleSection': self.object.get_categories(),
            'author': self.object.get_schema_author(),
            'copyrightYear': self.object.date_published.year,
            'dateCreated': self.object.get_date('dateCreated'),
            'dateModified': self.object.get_date('dateModified'),
            'datePublished': self.object.date_published,
            'headline': self.object.abstract[:50],
            'keywords': self.object.get_keywords(),
            'description': self.object.get_description(),
            'name': self.object.title,
            'url': self.object._get_full_url(url),
            'mainEntityOfPage': self.object._get_full_url(url),
            'publisher': self.object.get_domain(),
        }


class PostMixinImageObjectDetailView(PostMixinDetailView):
    def get_meta_image_object(self, context=None):
        return self.object.get_image_object()


class PostListView(MetadataMixin, ListView):
    model = Post
    title = "Some page"
    description = "This is an awesome page"
    image = "img/some_page_thumb.gif"
    url = "some/page/"
    extra_props = {"foo": "bar", "key": "value"}
    extra_custom_props = [("key", "foo", "bar"), ("property", "name", "value")]

    def get_schema(self, context=None):
        return {
            '@type': 'CollectionPage',
            'name': self.title,
            'url': reverse('post-list'),
            'mainEntity': {
                '@type': 'ItemList',
                'itemListElement': [
                    {
                        '@type': 'BlogPosting',
                        'image': self._get_full_url(self.image),
                        'articleBody': ' '.join(paragraphs(count=5, common=False)),
                        'author': {
                            '@type': 'Person',
                            'name': 'Joe Smith',
                        },
                        'copyrightYear': now().year,
                        'dateCreated': now() - timedelta(days=1),
                        'dateModified': now(),
                        'datePublished': now() - timedelta(days=1),
                        'headline': words(count=5, common=False),
                        'keywords': ','.join(words(count=5, common=False).split(' ')),
                        'description': words(count=5, common=False),
                        'name': words(count=5, common=False),
                        'url': reverse('post-list'),
                        'mainEntityOfPage': reverse('post-detail', kwargs={'slug': words(count=1, common=False)}),
                        'publisher': {
                            '@type': 'Organization',
                            'name': 'My Publisher',
                            'logo': Meta(schema={
                                '@type': 'ImageObject',
                                'url': self._get_full_url(self.image),
                            })
                        }
                    },
                    {
                        '@type': 'BlogPosting',
                        'image': self._get_full_url(self.image),
                        'articleBody': ' '.join(paragraphs(count=5, common=False)),
                        'author': {
                            '@type': 'Person',
                            'name': 'Joe Smith',
                        },
                        'copyrightYear': now().year,
                        'dateCreated': now() - timedelta(days=1),
                        'dateModified': now(),
                        'datePublished': now() - timedelta(days=1),
                        'headline': words(count=5, common=False),
                        'keywords': ','.join(words(count=5, common=False).split(' ')),
                        'description': words(count=5, common=False),
                        'name': words(count=5, common=False),
                        'url': reverse('post-list'),
                        'mainEntityOfPage': reverse('post-detail', kwargs={'slug': words(count=1, common=False)}),
                        'publisher': {
                            '@type': 'Organization',
                            'name': 'My Publisher',
                            'logo': Meta(schema={
                                '@type': 'ImageObject',
                                'url': self._get_full_url(self.image),
                            })
                        }
                    }
                ]}}
>>>>>>> 46a4396 (Add schema.org support)
