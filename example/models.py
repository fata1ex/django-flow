# coding: utf-8

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    content = models.TextField(verbose_name='content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    likes = generic.GenericRelation('Like', related_query_name='posts')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.title


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', verbose_name='user')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created at')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ('-created_at',)

    def __unicode__(self):
        return '{0} <3 {1}'.format(self.user, self.object_id)
