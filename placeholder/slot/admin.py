#-*- coding:utf-8 -*-

from django.conf import settings
from django.contrib import admin

from polymorphic.admin import \
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

import placeholder

from .. import PlaceholderAdmin
from .models import Slot, Portlet, SlotPortlet

GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS
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
    change_list_filter_template = "admin/filter_listing.html"
    list_display = ("id", "title", "polymorphic_ctype", )
    list_display_links = ("id", "title", )
    ordering = ("-id", )
    search_fields = ("title", )

    if GRAPPELLI_INSTALLED:
        change_list_template = "admin/change_list_filter_sidebar.html"

    def get_child_models(self):
        return PORTLETADMINS


admin.site.register(Portlet, MainPortletAdmin)


class SlotPortletInline(admin.TabularInline):
    extra = 1
    model = SlotPortlet
    raw_id_fields = ("portlet", )
    sortable_field_name = "ordering"


class SlotAdmin(PlaceholderAdmin):
    inlines = (SlotPortletInline, )


admin.site.register(Slot, SlotAdmin)


class SlotPlaceholder(object):
    fields = ("key", "description", )
    readonly_fields = ("key", )
    inlines = (SlotPortletInline, )


placeholder.register(SlotAdmin, SlotPlaceholder, 'portlets')
