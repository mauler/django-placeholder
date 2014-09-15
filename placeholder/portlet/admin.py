from json import dumps, loads

from django.contrib import admin
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django import forms

from placeholder.slot import admin as slot_admin

from .models import EasyPortlet
from .utils import extract_form_declaration, declare_fields, make_form_class


class EasyPortletAdmin(admin.ModelAdmin):

    class Media:
        js = ("easyportlet.js", )

    def get_form(self, request, obj=None, **kwargs):
        template_name = request.GET.get("template_name")

        if not template_name and obj:
            template_name = obj.template_name

        if template_name:
            source = open(template_name).read()
            data = extract_form_declaration(source)
            initial = {}
            if obj and obj.json_data:
                initial = loads(obj.json_data)

            for f in obj.file_set.all():
                initial[f.fieldname] = f.file

            fields = declare_fields(data.get('portlet', {}), initial)
            meta_fields = \
                ['template_name'] + [name for name, field in fields]

            class Meta:
                fields = meta_fields
                model = EasyPortlet

            form_class = make_form_class(fields, forms.ModelForm, Meta)

            return form_class

        return super(EasyPortletAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        files = {}
        validfiles = []
        cleaned_data = form.cleaned_data.copy()
        for key, val in cleaned_data.items():
            if isinstance(val, UploadedFile):
                del cleaned_data[key]
                files[key] = val
                validfiles.append(key)
            elif isinstance(val, File):
                del cleaned_data[key]
                validfiles.append(key)

        obj.json_data = dumps(cleaned_data)
        obj.save()
        obj.file_set.exclude(fieldname__in=validfiles).delete()
        for fieldname, uploadedfile in files.items():
            fo, created = obj.file_set.get_or_create(
                fieldname=fieldname, defaults={'file': uploadedfile})
            if not created:
                fo.file = uploadedfile
                fo.save(update_fields=['file'])

slot_admin.site.register(EasyPortlet, EasyPortletAdmin)
