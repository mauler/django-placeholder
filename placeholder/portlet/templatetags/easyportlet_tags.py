#-*- coding:utf-8 -*-

from os.path import join

from django.conf import settings
from django import template

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument

from .. import models


register = template.Library()


class EasyPortlet(InclusionTag):
    name = 'easyportlet'
    options = Options(
        Argument('slot', required=True, resolve=True),
        Argument('template_name', required=True, resolve=True),
        Argument('title', required=True, resolve=True),
    )
    template = 'slot/portlet.html'

    def get_context(self, context, slot, template_name, title):
        template_name = join(
            settings.EASYPORTLET_TEMPLATES_PATH,
            template_name)
        qs = slot.slotportlet_set.filter(
            portlet__easyportlet__template_name=template_name)
        qs = qs.distinct()
        qs = qs[:1]
        if qs.exists():
            sp = qs.get()
            portlet = sp.portlet
        else:
            portlet = models.EasyPortlet.objects.create(
                title=title,
                template_name=template_name)
            slot.slotportlet_set.create(portlet=portlet, ordering=0)
        context.update({'portlet': portlet})
        return context


register.tag(EasyPortlet)
