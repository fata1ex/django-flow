# coding: utf-8

import json
import logging

from django.core.cache import cache
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import Http404

from django.db import models

logger = logging.getLogger('dobro')


class FlowQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class FlowConfiguration(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='is active')

    name = models.CharField(max_length=20, verbose_name='name')
    configuration = models.TextField(verbose_name='configuration')

    default_configuration = '''{"element_list": {}}'''
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
        configuration_object = cache.get(cls.cache_key)
        if configuration_object is None:
            try:
                configuration_object = cls.objects.get(is_active=True)
                cache.set(cls.cache_key, configuration_object)

            except ObjectDoesNotExist:
                configuration_object = cls.default_configuration
                cache.set(cls.cache_key, configuration_object)

            except MultipleObjectsReturned:
                logger.exception('Too many flow configurations!')
                raise Http404

        return json.loads(configuration_object.configuration)


from .signals import init_signals
init_signals()
