#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument


register = template.Library()


class Portlet(InclusionTag):
    name = 'render_portlet'
    template = 'slot/portlet.html'
    options = Options(
        Argument(
            "portlet", required=False, resolve=True),
    )

    def get_context(self, context, portlet):
        c = portlet.get_context(context)
        context.update(c)
        return context


register.tag(Portlet)
