# coding: utf-8

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _

from placeholder.slot.models import Portlet


class CTPortlet(Portlet):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    template_name = models.CharField(
        default="portlet/default.html",
        verbose_name=_("Template"),
        max_length=100,
    )


class StaticPortlet(Portlet):
    template_name = "portlet/static.html"
    content = models.TextField()
