from json import dumps, loads

from django.contrib import admin
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
            if obj:
                initial = loads(obj.json_data)

            fields = declare_fields(data.get('portlet', {}), initial)
            meta_fields = \
                ['template_name', 'title'] + [name for name, field in fields]

            class Meta:
                fields = meta_fields
                model = EasyPortlet

            form_class = make_form_class(fields, forms.ModelForm, Meta)

            return form_class

        return super(EasyPortletAdmin, self).get_form(request, obj, **kwargs)

    def save_form(self, request, form, change):
        portlet = form.save(commit=False)
        portlet.json_data = dumps(form.cleaned_data)
        return portlet


slot_admin.site.register(EasyPortlet, EasyPortletAdmin)
