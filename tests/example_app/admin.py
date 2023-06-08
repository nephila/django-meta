from django.contrib import admin

from .models import Comment, Post, Publisher

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Publisher)
