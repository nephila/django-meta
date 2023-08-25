from datetime import timedelta

import django
import pytest
from django.utils.text import slugify
from django.utils.timezone import now

from tests.example_app.models import Post

try:
    from asgiref.sync import sync_to_async
    from django.test import AsyncRequestFactory, override_settings
except ImportError:
    # stub to avoid decorator failures
    def sync_to_async(__):
        return

    pytestmark = pytest.mark.skip("asgiref not installed, skipping async tests")

minversion = pytest.mark.skipif(django.VERSION < (3, 1), reason="at least Django 3.1 required")


@sync_to_async
def get_post(title):
    post, __ = Post.objects.get_or_create(
        title=title,
        og_title="og {title}".format(title=title),
        twitter_title="twitter {title}".format(title=title),
        schemaorg_title="schemaorg {title}".format(title=title),
        slug=slugify(title),
        abstract="post abstract",
        meta_description="post meta",
        meta_keywords="post keyword1,post keyword 2",
        date_published_end=now() + timedelta(days=2),
        text="post text",
        image_url="/path/to/image",
    )
    return post


@sync_to_async
def delete_post(post):
    post.delete()


@sync_to_async
def get_meta(post, request=None):
    return post.as_meta(request)


@minversion
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_mixin_on_asgi():
    with override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="http", META_USE_OG_PROPERTIES=True):
        post = await get_post("first post")
        meta = await get_meta(post)
        assert meta.title == "first post"
        assert meta.og_title == "og first post"


@minversion
@pytest.mark.asyncio
@pytest.mark.django_db
async def test_mixin_on_asgi_request():
    with override_settings(META_USE_SITES=True, META_SITE_PROTOCOL="http", META_USE_OG_PROPERTIES=True):
        request = AsyncRequestFactory().get("/")
        post = await get_post("first post")
        meta = await get_meta(post, request)
        assert meta.title == "first post"
        assert meta.og_title == "og first post"
