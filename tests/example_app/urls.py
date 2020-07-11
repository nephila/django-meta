# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django.views.static
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from .views import PostDetailView, PostListView, PostMixinDetailView, PostMixinImageObjectDetailView

try:
    from django.views.i18n import JavaScriptCatalog
    javascript_catalog = JavaScriptCatalog.as_view()
except ImportError:
    from django.views.i18n import javascript_catalog

admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', javascript_catalog),  # NOQA
    url(r'^mixin/(?P<slug>\w[-\w]*)/$', PostMixinDetailView.as_view(), name='post-detail-mixinx'),
    url(r'^mixin_image/(?P<slug>\w[-\w]*)/$', PostMixinImageObjectDetailView.as_view(), name='post-detail-image-mixinx'),
    url(r'^(?P<slug>\w[-\w]*)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^$', PostListView.as_view(), name='post-list'),
]
try:
    urlpatterns.insert(0, url(r'^admin/', admin.site.urls)),  # NOQA
except Exception:
    urlpatterns.insert(0, url(r'^admin/', include(admin.site.urls))),  # NOQA
