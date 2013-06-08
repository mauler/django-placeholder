#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from .views import placeholder_save


urlpatterns = patterns('',
    url(r'^save/$', placeholder_save, name="placeholder_save"),
)
