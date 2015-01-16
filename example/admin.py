# coding: utf-8

from django.contrib import admin

from example.models import Post, Like


class PostAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created_at']
    date_hierarchy = 'created_at'


class LikeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created_at']
    list_filter = ['user']
    date_hierarchy = 'created_at'

    list_select_related = ['user']

    def get_queryset(self, request):
        return super(LikeAdmin, self).get_queryset(request).prefetch_related('posts')


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
