import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import re_path

from .views import PostDetailView, PostListView, PostMixinDetailView, PostMixinImageObjectDetailView

try:
    from django.views.i18n import JavaScriptCatalog

    javascript_catalog = JavaScriptCatalog.as_view()
except ImportError:
    from django.views.i18n import javascript_catalog

admin.autodiscover()

urlpatterns = [
    re_path(
        r"^media/(?P<path>.*)$",
        django.views.static.serve,  # NOQA
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
    re_path(r"^jsi18n/(?P<packages>\S+?)/$", javascript_catalog),  # NOQA
    re_path(r"^mixin/(?P<slug>\w[-\w]*)/$", PostMixinDetailView.as_view(), name="post-detail-mixinx"),
    re_path(
        r"^mixin_image/(?P<slug>\w[-\w]*)/$", PostMixinImageObjectDetailView.as_view(), name="post-detail-image-mixinx"
    ),
    re_path(r"^(?P<slug>\w[-\w]*)/$", PostDetailView.as_view(), name="post-detail"),
    re_path(r"^$", PostListView.as_view(), name="post-list"),
]
try:
    urlpatterns.insert(0, re_path(r"^admin/", admin.site.urls)),  # NOQA
except Exception:
    urlpatterns.insert(0, re_path(r"^admin/", include(admin.site.urls))),  # NOQA
