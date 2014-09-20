from collections import OrderedDict
from json import loads, dumps
import re

from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model
from django import forms

from bs4 import BeautifulSoup
import yaml


def get_form_declaration(template_name):
    source = open(template_name).read()
    return extract_form_declaration(source)


def set_metadata(instance, data):
    files = {}
    validfiles = []
    for key, val in data.items():
        if isinstance(val, UploadedFile):
            del data[key]
            files[key] = val
            validfiles.append(key)
        elif isinstance(val, File):
            del data[key]
            validfiles.append(key)
        elif isinstance(val, File):
            del data[key]
            validfiles.append(key)
        elif isinstance(val, Model):
            del data[key]

    instance.json_data = dumps(data)
    instance.save(update_fields=['json_data'])
    instance.file_set.exclude(fieldname__in=validfiles).delete()
    for fieldname, uploadedfile in files.items():
        fo, created = instance.file_set.get_or_create(
            fieldname=fieldname, defaults={'file': uploadedfile})
        if not created:
            fo.file = uploadedfile
            fo.save(update_fields=['file'])


def load_metadata(instance):
    meta = {}
    if instance.json_data:
        data = loads(instance.json_data)
        for key in ('id', "template_name", ):
            if key in data:
                del data[key]
        meta.update(data)

    for f in instance.file_set.all():
        meta[f.fieldname] = f.file

    return meta


def apply_metadata(instance):
    for k, v in load_metadata(instance).items():
        setattr(instance, k, v)


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


def get_helper_fields(text):
    fields = []
    for name in text.lower().split(","):
        field = None
        if name == 'title':
            field = {name: {'CharField': {'required': True}}}
        elif name == 'price':
            field = {name: {'CharField': {'required': True}}}
        elif name == 'date':
            field = {name: {'DateField': {'required': True}}}
        elif name == 'subtitle':
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
    return fields


def get_helper_declaration(text):
    parts = text.split("|", 1)
    data = {'collection': {}}
    data['portlet'] = get_helper_fields(parts[0])
    if len(parts) > 1:
        data['collection'] = get_helper_fields(parts[1])
    return data


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
