#-*- coding:utf-8 -*-

from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
    'placeholder.views',
    url(r'^multiedit/save/$', "multiedit_save", name="multiedit_save"),
    url(r'^save/$', "placeholder_save", name="placeholder_save"),
)
