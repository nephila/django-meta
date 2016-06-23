# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.views.generic import DetailView, ListView

from meta.views import MetadataMixin

from .models import Post


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta()
        return context


class PostMixinDetailView(MetadataMixin, DetailView):
    model = Post

    def get_meta_keywords(self, context):
        return self.object.meta_keywords.split(',')

    def get_meta_title(self, context):
        return self.object.title

    def get_meta_description(self, context):
        return self.object.meta_description

    def get_meta_gplus_publisher(self, context):
        return '+FooPub'

    def get_meta_image(self, context):
        return self.object.image_url


class PostListView(MetadataMixin, ListView):
    model = Post
    title = 'Some page'
    description = 'This is an awesome page'
    image = 'img/some_page_thumb.gif'
    url = 'some/page/'
