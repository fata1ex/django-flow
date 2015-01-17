# coding: utf-8

from jsonfield import JSONField

from django.core.cache import cache

from django.db import models


class FlowQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class FlowConfiguration(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='is active')

    name = models.CharField(max_length=20, verbose_name='name')
    configuration = JSONField(verbose_name='configuration')

    cache_key = 'flow_configuration'

    objects = FlowQuerySet.as_manager()

    class Meta:
        verbose_name = 'Flow Configuration'
        verbose_name_plural = 'Flow Configurations'

    def __unicode__(self):
        return self.name

    def activate(self, commit=True):
        self.is_active = True
        if commit:
            self.save()

    def deactivate(self, commit=True):
        self.is_active = False
        if commit:
            self.save()

    @classmethod
    def get_configuration(cls):
        configuration = cache.get(cls.cache_key)
        if configuration is None:
            try:
                configuration_object = cls.objects.active()[0]
                configuration = configuration_object.configuration

            except IndexError:
                configuration = {}

        cache.set(cls.cache_key, configuration)
        return configuration


from .signals import init_signals
init_signals()
