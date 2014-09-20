#-*- coding:utf-8 -*-

from placeholder.slot import admin

from .models import CTPortlet, StaticPortlet


admin.site.register(StaticPortlet)


admin.site.register(CTPortlet)
