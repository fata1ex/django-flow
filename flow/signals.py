# coding: utf-8

from django.db.models.signals import pre_save
from django.dispatch import receiver

from flow.models import FlowConfiguration


def init_signals():
    pass


@receiver(pre_save, sender=FlowConfiguration)
def track_active_configuration(sender, **kwargs):
    configuration = kwargs['instance']
    if configuration.is_active:
        for conf in FlowConfiguration.objects.active().exclude(id=configuration.id):
            conf.deactivate(commit=False)

    elif not FlowConfiguration.objects.active().exists():
        # You are not allowed to deactivate last configuration
        configuration.activate(commit=False)

    return
