#!/usr/bin/env python
#-*- coding:utf-8 -*-

from json import dumps
import md5

from django.core.urlresolvers import reverse
from django.utils.html import escape
from django import template

from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiKeywordArgument


register = template.Library()


class PlaceholderMultiedit(Tag):
    name = 'ph_multiedit'
    options = Options(
        Argument('multiedit', required=False, default=False),
    )

    def render_tag(self, context, multiedit):
        arg = multiedit and "true" or "false"
        return "<script>var __placeholder_multiedit = %s;</script>" % arg


register.tag(PlaceholderMultiedit)


class PlaceholderField(Tag):
    name = 'ph_field_tagattrs'
    options = Options(
        Argument('instance', required=True),
        Argument('field', required=True),
    )

    def render_tag(self, context, instance, field):
        if 'request' in context:
            user = context['request'].user
            perm = instance._meta.get_change_permission()
            valid_user = user.is_authenticated() and \
                user.is_staff and \
                user.has_perm(perm)
            if not valid_user:
                return u""

        save_url = reverse("placeholder_save")

        meta = dumps({
            'app_label': instance._meta.app_label,
            'model_name': instance.__class__.__name__,
            'model_pk': instance.pk,
            'model_field': field,
            'save_url': save_url,
        })

        meta = escape(meta)
        md5hash = md5.new(meta).hexdigest()
        args = (meta, md5hash)
        return u"data-placeholder-field=\"%s\" " \
            u"data-placeholder-md5hash=\"%s\"" % args


register.tag(PlaceholderField)


class PlaceholderInstance(Tag):
    name = 'ph_instance_tagattrs'
    options = Options(
        Argument('instance', required=True),
        Argument('placeholder_admin', default=None, required=False),
    )

    def render_tag(self, context, instance, placeholder_admin):
        if 'request' in context:
            user = context['request'].user
            perm = instance._meta.get_change_permission()
            valid_user = user.is_authenticated() and \
                user.is_staff and \
                user.has_perm(perm)
            if not valid_user:
                return u""

        args = (instance._meta.app_label, instance._meta.object_name.lower())
        change_url = reverse(
            "admin:%s_%s_change" % args, args=(instance.pk, ))

        meta = dumps({
            'app_label': instance._meta.app_label,
            'model_name': instance.__class__.__name__,
            'model_pk': instance.pk,
            'placeholder_admin': placeholder_admin,
            'admin_change_url': change_url
        })
        meta = escape(meta)
        md5hash = md5.new(meta).hexdigest()
        args = (meta, md5hash)
        return u"data-placeholder-instance=\"%s\" " \
            u"data-placeholder-md5hash=\"%s\"" % args


register.tag(PlaceholderInstance)


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


class PlaceholderRT(Tag):
    name = 'placeholder_rt'
    options = Options(
        Argument('model_object', required=True),
        Argument('model_attribute', required=True, resolve=False),
        MultiKeywordArgument('kwords', required=False, resolve=True)
    )

    def render_tag(self, context, model_object, model_attribute, kwords):
        value = getattr(model_object, model_attribute)
        meta = escape(dumps({
            'app_label': model_object._meta.app_label,
            'model_name': model_object.__class__.__name__,
            'model_attribute': model_attribute,
            'model_pk': model_object.pk
        }))
        params = {'tag': 'div', 'content': value, 'meta': meta}
        params.update(kwords)
        value = (
            u"<%(tag)s class=\"%(class)s\" data-placeholder-richtext "
            u"data-placeholder-meta=\"%(meta)s\">"
            u"%(content)s</%(tag)s>") % params
        return value


register.tag(PlaceholderRT)


class PlaceholderObjects(Tag):
    name = 'placeholder_objects'
    options = Options(
        Argument('queryset', required=True),
        blocks=[('endplaceholder_objects', 'nodelist', )],
    )

    def render_tag(self, context, queryset, nodelist):
        meta = dumps({
            'app_label': queryset.model._meta.app_label,
            'model_name': queryset.model.__class__.__name__,
        })
        output = nodelist.render(context)
        source = \
            u"<!--placeholder:objects:meta:{meta}-->" \
            u"{output}" \
            u"<!--/placeholder:objects:meta-->"
        output = source.format(
            meta=meta,
            output=output)
        return output

register.tag(PlaceholderObjects)
