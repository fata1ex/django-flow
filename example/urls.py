# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    'example.views',
    url(r'^$', 'index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
