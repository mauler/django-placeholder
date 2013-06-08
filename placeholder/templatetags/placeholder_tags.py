#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument

from simplejson import dumps


register = template.Library()

class Placeholder(Tag):
    options = Options(
        Argument('model_object', required=True),
        Argument('model_attribute', required=True, resolve=False)
    )

    def render_tag(self, context, model_object, model_attribute):
        value = getattr(model_object, model_attribute)
        #my_model = get_model(my_instance._meta.app_label, my_instance.__class__.__name__)
        meta = dumps({
            'app_label': model_object._meta.app_label,
            'model_name': model_object.__class__.__name__,
            'model_attribute': model_attribute,
            'model_pk': model_object.pk
        })
        value = u"<!--django:placeholder:%s-->%s<!--/django:placeholder-->" % \
            (meta, value)
        return value


register.tag(Placeholder)
