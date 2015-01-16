# coding: utf-8

from django.contrib import admin

from flow.models import FlowConfiguration


class FlowConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']


admin.site.register(FlowConfiguration, FlowConfigurationAdmin)
