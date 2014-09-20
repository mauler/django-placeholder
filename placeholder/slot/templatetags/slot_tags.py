#-*- coding:utf-8 -*-

from django.db.models import Model
from django import template

from classytags.core import Options
from classytags.helpers import InclusionTag, AsTag
from classytags.arguments import MultiValueArgument, Argument

from .. import models


register = template.Library()


def get_key(context, keys):
    if not keys:
        if 'request' in context:
            keys = context['request'].get_full_path().split("/")
        else:
            keys = ['norequest']

    parts = []
    for part in [k for k in keys if k]:
        if isinstance(part, Model):
            key = u"%s,%s,%d" % (
                part._meta.app_label, part.__class__.__name__, part.pk)
        else:
            key = unicode(part)
        parts.append(key)

    key = u"|".join([unicode(i) for i in parts])
    return key


class GetSlot(AsTag):
    name = 'get_slot'
    options = Options(
        MultiValueArgument('keys', required=False, resolve=True),
        'as',
        Argument('varname', required=False, resolve=False, default="slot")
    )

    def get_value(self, context, keys):
        key = get_key(context, keys)

        slot, created = models.Slot.objects.get_or_create(key=key)

        return slot


register.tag(GetSlot)


class RenderSlot(InclusionTag):
    name = 'render_slot'
    template = 'slot/slot.html'
    options = Options(
        MultiValueArgument('keys', required=False, resolve=True),
    )

    def get_context(self, context, keys):
        if keys and isinstance(keys[0], models.Slot):
            slot = keys[0]

        else:
            key = get_key(context, keys)
            slot, created = models.Slot.objects.get_or_create(key=key)

        context.update({
            "slot": slot})

        return context


register.tag(RenderSlot)
