#-*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, url

from .views import placeholder_save


urlpatterns = patterns(
    '',
    url(r'^save/$', placeholder_save, name="placeholder_save"),
)
