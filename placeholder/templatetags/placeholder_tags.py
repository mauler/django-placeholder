#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument

from simplejson import dumps


register = template.Library()


class Placeholder(Tag):
    name = 'placeholder'
    options = Options(
        Argument('model_object', required=True),
        Argument('model_attribute', required=True, resolve=False)
    )

    def render_tag(self, context, model_object, model_attribute):
        value = getattr(model_object, model_attribute)
        meta = dumps({
            'app_label': model_object._meta.app_label,
            'model_name': model_object.__class__.__name__,
            'model_attribute': model_attribute,
            'model_pk': model_object.pk
        })
        value = u"<!--placeholder:text:%s-->%s<!--/placeholder:text-->" % \
            (meta, value)
        return value


register.tag(Placeholder)


class PlaceholderInstance(Tag):
    name = 'placeholder_instance'
    options = Options(
        Argument('model_object', required=True),
        blocks=[('endplaceholder_instance', 'nodelist', )],
    )

    def render_tag(self, context, model_object, nodelist):
        if model_object is None:
            return ""

        meta = dumps({
            'app_label': model_object._meta.app_label,
            'model_name': model_object.__class__.__name__,
            'model_pk': model_object.pk
        })
        output = nodelist.render(context)
        output = \
            (
                u"<!--placeholder:instance:{model_name}:{pk}-->"  \
                u"<!--placeholder:instance:meta:{meta}-->" \
                u"{output}" \
                u"<!--/placeholder:instance:meta-->" \
                u"<!--/placeholder:instance:{model_name}:{pk}-->").format(
                    pk=model_object.pk, meta=meta,
                    model_name=model_object.__class__.__name__, output=output)
        return output

register.tag(PlaceholderInstance)


class PlaceholderObjects(Tag):
    name = 'placeholder_objects'
    options = Options(
        Argument('app_label', required=True),
        Argument('model_name', required=True),
        blocks=[('endplaceholder_objects', 'nodelist', )],
    )

    def render_tag(self, context, app_label, model_name, nodelist):
        meta = dumps({
            'app_label': app_label,
            'model_name': model_name,
        })
        output = nodelist.render(context)
        output = \
            (
                u"<!--placeholder:objects:meta:{meta}-->" \
                u"{output}" \
                u"<!--/placeholder:objects:meta-->").format(
                    meta=meta, output=output)
        return output

register.tag(PlaceholderObjects)
