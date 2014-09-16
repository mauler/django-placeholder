from functools import partial
from json import dumps, loads

from django.contrib.admin.util import flatten_fieldsets
from django.contrib import admin
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Model
from django.forms.models import inlineformset_factory
from django import forms

from placeholder.slot import admin as slot_admin

from .models import EasyPortlet, Item
from .utils import extract_form_declaration, declare_fields, make_form_class


class InlineModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.get("instance"):
            obj = kwargs['instance']
            initial = kwargs.get('initial', {})

            if obj.json_data:
                initial.update(loads(obj.json_data))

            for f in obj.file_set.all():
                initial[f.fieldname] = f.file

            kwargs['initial'] = initial

            from pprint import pprint
            pprint(initial)

        super(InlineModelForm, self).__init__(*args, **kwargs)

    def post_save(self, obj):
        cleaned_data = self.cleaned_data.copy()
        files = {}
        validfiles = []
        for key, val in cleaned_data.items():
            if isinstance(val, UploadedFile):
                del cleaned_data[key]
                files[key] = val
                validfiles.append(key)
            elif isinstance(val, File):
                del cleaned_data[key]
                validfiles.append(key)
            elif isinstance(val, File):
                del cleaned_data[key]
                validfiles.append(key)
            elif isinstance(val, Model):
                del cleaned_data[key]

        obj.json_data = dumps(cleaned_data)
        obj.save(update_fields=['json_data'])
        obj.file_set.exclude(fieldname__in=validfiles).delete()
        for fieldname, uploadedfile in files.items():
            fo, created = self.instance.file_set.get_or_create(
                fieldname=fieldname, defaults={'file': uploadedfile})
            if not created:
                fo.file = uploadedfile
                fo.save(update_fields=['file'])

    def save(self, commit=True):
        obj = super(InlineModelForm, self).save(commit)
        obj._form = self
        return obj


class ItemInline(admin.StackedInline):
    # formset = ItemInlineFormSet
    model = Item
    sortable_field_name = "position"

    def get_formset(self, request, obj=None, **kwargs):
        if self.declared_fieldsets:
            fields = flatten_fieldsets(self.declared_fieldsets)
        else:
            fields = None
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(self.get_readonly_fields(request, obj))
        if self.exclude is None and \
                hasattr(self.form, '_meta') and self.form._meta.exclude:
            # Take the custom ModelForm's Meta.exclude into account only if the
            # InlineModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)
        # if exclude is an empty list we use None, since that's the actual
        # default
        exclude = exclude or None
        can_delete = \
            self.can_delete and self.has_delete_permission(request, obj)
        defaults = {
            "form": self.get_form(request, obj),
            "formset": self.formset,
            "fk_name": self.fk_name,
            "fields": fields,
            "exclude": exclude,
            "formfield_callback": partial(
                self.formfield_for_dbfield, request=request),
            "extra": self.extra,
            "max_num": self.max_num,
            "can_delete": can_delete,
        }
        defaults.update(kwargs)
        return inlineformset_factory(self.parent_model, self.model, **defaults)

    def get_form(self, request, obj=None, **kwargs):
        template_name = request.GET.get("template_name")

        if not template_name and obj:
            template_name = obj.template_name

        if template_name:
            source = open(template_name).read()
            data = extract_form_declaration(source)
            initial = {}
            # if obj and obj.json_data:
            #     initial = loads(obj.json_data)

            # for f in obj.file_set.all():
            #     initial[f.fieldname] = f.file

            fields = declare_fields(data.get('portlet', {}), initial)
            meta_fields = \
                ['position', 'title'] + [name for name, field in fields]

            class Meta:
                fields = meta_fields
                model = self.model

            form_class = make_form_class(fields, InlineModelForm, Meta)

            return form_class

        return super(ItemInline, self).get_form(request, obj, **kwargs)


class EasyPortletAdmin(admin.ModelAdmin):
    inlines = (ItemInline, )

    class Media:
        js = ("easyportlet.js", )

    # def get_inline_instances(self, request, obj=None):
    #     inline_instances = []
    #     for inline_class in self.inlines:
    #         inline = inline_class(self.model, self.admin_site)
    #         if request:
    #             if not (inline.has_add_permission(request) or
    #                     inline.has_change_permission(request, obj) or
    #                     inline.has_delete_permission(request, obj)):
    #                 continue
    #             if not inline.has_add_permission(request):
    #                 inline.max_num = 0
    #         inline_instances.append(inline)

    #     return inline_instances

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
                ['template_name', 'title'] + [name for name, field in fields]

            class Meta:
                fields = meta_fields
                model = self.model

            form_class = make_form_class(fields, forms.ModelForm, Meta)

            return form_class

        return super(EasyPortletAdmin, self).get_form(request, obj, **kwargs)

    def get_object(self, request, object_id):
        obj = super(EasyPortletAdmin, self).get_object(request, object_id)
        obj.template_name = request.GET.get("template_name", obj.template_name)
        return obj

    def save_formset(self, request, form, formset, change):
        for obj in formset.save():
            obj._form.post_save(obj)

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
