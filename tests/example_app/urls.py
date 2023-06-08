from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

from .views import PostDetailView, PostListView, PostMixinDetailView, PostMixinImageObjectDetailView

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("media/<str:path>", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path("mixin/<slug:slug>/", PostMixinDetailView.as_view(), name="post-detail-mixinx"),
    path("mixin_image/<slug:slug>/", PostMixinImageObjectDetailView.as_view(), name="post-detail-image-mixinx"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("", PostListView.as_view(), name="post-list"),
]
