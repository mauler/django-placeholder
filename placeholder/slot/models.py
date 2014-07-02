#-*- coding:utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic import PolymorphicModel


class Portlet(PolymorphicModel):
    template_name = None
    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )

    class Meta:
        ordering = ("-id", )

    def __unicode__(self):
        return self.title

    def get_context(self, context):
        return {}


class Slot(models.Model):
    key = models.TextField(
        db_index=True,
        unique=True,
        verbose_name=_("Key"),
    )

    description = models.TextField(
        _(u"Description"),
        blank=True,
    )

    portlets = models.ManyToManyField(
        "Portlet",
        through='SlotPortlet',
    )

    def __unicode__(self):
        return self.description or self.key

    def get_portlets(self):
        return self.portlets.order_by("slotportlet__ordering")


class SlotPortlet(models.Model):
    slot = models.ForeignKey("Slot")
    portlet = models.ForeignKey("Portlet")
    ordering = models.PositiveIntegerField(default=999)

    class Meta:
        ordering = ("ordering", )
        unique_together = ("slot", "portlet", )

    def __unicode__(self):
        return self.portlet.title
