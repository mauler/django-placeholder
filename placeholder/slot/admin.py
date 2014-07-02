#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin

from polymorphic.admin import \
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models import Slot, Portlet, SlotPortlet


PORTLETADMINS = []


class site:
    @staticmethod
    def register(model, modeladmin=None):
        if modeladmin is None:
            name = "%sAdmin" % model.__class__.__name__
            modeladmin = \
                type(name, (PortletAdmin, ), {})
        PORTLETADMINS.append((model, modeladmin))


class PortletAdmin(PolymorphicChildModelAdmin):
    base_model = Portlet


class MainPortletAdmin(PolymorphicParentModelAdmin):
    base_model = Portlet

    def get_child_models(self):
        return PORTLETADMINS


admin.site.register(Portlet, MainPortletAdmin)


class SlotPortletInline(admin.TabularInline):
    extra = 1
    model = SlotPortlet
    raw_id_fields = ("portlet", )


class SlotAdmin(admin.ModelAdmin):
    inlines = (SlotPortletInline, )


admin.site.register(Slot, SlotAdmin)
