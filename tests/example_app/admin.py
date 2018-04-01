# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib import admin

from .models import Comment, Post, Publisher

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Publisher)
