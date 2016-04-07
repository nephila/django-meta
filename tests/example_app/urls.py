# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import django.views.i18n
import django.views.static
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from .views import PostDetailView, PostListView, PostMixinDetailView


admin.autodiscover()

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,  # NOQA
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^jsi18n/(?P<packages>\S+?)/$', django.views.i18n.javascript_catalog),  # NOQA
    url(r'^mixin/(?P<slug>\w[-\w]*)/$', PostMixinDetailView.as_view(), name='post-detail-mixinx'),
    url(r'^(?P<slug>\w[-\w]*)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'^$', PostListView.as_view(), name='post-list'),
]
urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
)
