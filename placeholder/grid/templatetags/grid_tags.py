#-*- coding:utf-8 -*-

from django import template

from classytags.core import Options
from classytags.helpers import InclusionTag, AsTag
from classytags.arguments import MultiValueArgument, Argument

from placeholder.slot.templatetags.slot_tags import get_key
from .. import models


register = template.Library()


class GetGrid(AsTag):
    name = 'get_grid'
    options = Options(
        MultiValueArgument('keys', required=False, resolve=False),
        'as',
        Argument('varname', required=False, resolve=False, default="grid")
    )

    def get_value(self, context, keys):
        key = get_key(context, keys)

        grid, created = models.Grid.objects.get_or_create(key=key)

        return grid


register.tag(GetGrid)


class RenderGrid(InclusionTag):
    name = 'render_grid'
    template = 'grid/grid.html'
    options = Options(
        MultiValueArgument('keys', required=False, resolve=True),
    )

    def get_context(self, context, keys):
        if keys and isinstance(keys[0], models.Grid):
            grid = keys[0]

        else:
            key = get_key(context, keys)
            grid, created = models.Grid.objects.get_or_create(key=key)

        context.update({
            "grid": grid})

        return context


register.tag(RenderGrid)
