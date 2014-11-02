# coding: utf-8

from django.db.models import signals

from .__init__ import world


def multiedit_post_init(sender, instance, *args, **kwargs):
    multiedit = getattr(world, "__placeholder_multiedit", {})
    k = instance._meta.app_label
    if k in multiedit:
        multiedit = multiedit[k]
        k = instance.__class__.__name__
        if k in multiedit:
            multiedit = multiedit[k]
            for attr, value in multiedit.items():
                setattr(instance, attr, value)


signals.post_init.connect(multiedit_post_init)
