# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import url

from .views import PostDetailView, PostMixinDetailView

urlpatterns = [
    url(r'^mixin/(?P<slug>\w[-\w]*)/$', PostMixinDetailView.as_view(), name='post-detail-mixinx'),
    url(r'^(?P<slug>\w[-\w]*)/$', PostDetailView.as_view(), name='post-detail'),
]
