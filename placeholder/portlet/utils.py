from collections import OrderedDict
import re

from django import forms

from bs4 import BeautifulSoup
import yaml


def extract_form_declaration(source):
    text = "PORTLET:YAML:"
    if text in source:
        soup = BeautifulSoup(source)
        soup = soup.find(text=re.compile(text))
        soup = soup.replace(text, "").strip()
        return yaml.load(soup)
    text = "PORTLET:HELPER:"
    if text in source:
        soup = BeautifulSoup(source)
        soup = soup.find(text=re.compile(text))
        soup = soup.replace(text, "").strip()
        return get_helper_declaration(soup)

    return {}


def get_helper_declaration(text):
    fields = []
    for name in text.lower().split(","):
        field = None
        if name == 'title':
            field = {name: {'CharField': {'required': True}}}
        elif name == 'hat':
            field = {name: {'CharField': {'required': True}}}
        elif name == 'image':
            field = {name: {'ImageField': {'required': True}}}
        elif name == 'url':
            field = {name: {'URLField': {'required': True}}}
        elif name == 'urloptional':
            name = 'url'
            field = {name: {'URLField': {'required': False}}}
        elif name == 'text':
            field = \
                {name:
                    {'CharField': {'required': True, 'widget': "Textarea"}}}
        if field is not None:
            fields.append(field)
    return {"portlet": fields}


def declare_fields(data, initial={}):
    if isinstance(data, dict):
        data = [{key: data[key]} for key in data]

    attrs = []

    for i in data:
        params = {}
        for name, params in i.items():
            for field, params in params.items():
                field_class = getattr(forms.fields, field)
                if 'widget' in params:
                    widget = getattr(forms.widgets, params['widget'])
                    params['widget'] = widget()

                if name in initial:
                    params['initial'] = initial[name]

                attrs.append((name, field_class(**params)))

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
