from collections import OrderedDict
import re

from django import forms

from bs4 import BeautifulSoup
import yaml


def extract_form_declaration(source):
    text = "PORTLET:META:"
    if not text in source:
        return {}

    soup = BeautifulSoup(source)
    soup = soup.find(text=re.compile(text))
    soup = soup.replace(text, "").strip()
    return yaml.load(soup)


def declare_fields(data, initial={}):
    if isinstance(data, dict):
        data = [{key: data[key]} for key in data]

    attrs = []

    for i in data:
        params = {}
        for name, params in i.items():
            for field, params in params.items():
                if 'widget' in params:
                    widget = getattr(forms.widgets, params['widget'])
                    params['widget'] = widget()

                if name in initial:
                    params['initial'] = initial[name]

                attrs.append((name, getattr(forms.fields, field)(**params)))

    return attrs


def make_form_class(fields, baseform=forms.Form, meta=None):
    attrs = OrderedDict()

    for name, field in fields:
        attrs[name] = field

    if meta:
        attrs['Meta'] = meta

    form_class = type("PortletForm", (baseform, ), attrs)

    return form_class


def declare_form(data, baseform=forms.Form, meta=None):
    fields = declare_fields(data)
    form_class = make_form_class(fields, baseform, meta)
    return form_class
