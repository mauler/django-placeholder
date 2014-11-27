from functools import partial

from django.conf import settings
from django.contrib.admin.util import flatten_fieldsets
from django.contrib import admin
from django.forms.models import inlineformset_factory
from django import forms

from placeholder.slot import admin as slot_admin

from .helpers import get_template_name
from .models import EasyPortlet, Item
from .utils import \
    declare_fields, make_form_class, load_metadata, set_metadata, \
    get_form_declaration


GRAPPELLI_INSTALLED = 'grappelli' in settings.INSTALLED_APPS


class InlineModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.get("instance"):
            obj = kwargs['instance']
            initial = kwargs.get('initial', {})
            initial.update(load_metadata(obj))
            kwargs['initial'] = initial

        super(InlineModelForm, self).__init__(*args, **kwargs)
        if GRAPPELLI_INSTALLED:
            self.fields['position'].widget = forms.HiddenInput()

    def save(self, commit=True):
        obj = super(InlineModelForm, self).save(commit)
        obj._form_cleaned_data = self.cleaned_data
        return obj


class ItemInline(admin.StackedInline):
    extra = 0
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
        template_name = get_template_name(request, obj)

        if template_name:
            data = get_form_declaration(template_name)
            initial = {}
            fields = declare_fields(data.get('collection', {}), initial)
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
        css = {
            'all': ('easyportlet.css', )
        }
        js = ("easyportlet.js", )

    def get_inline_instances(self, request, obj=None):
        template_name = get_template_name(request, obj)

        if template_name:
            data = get_form_declaration(template_name)
            if not data.get("collection"):
                return []

        return super(EasyPortletAdmin, self).get_inline_instances(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        template_name = get_template_name(request, obj)

        if template_name:
            data = get_form_declaration(template_name)
            initial = load_metadata(obj)
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
            set_metadata(obj, obj._form_cleaned_data)

    def save_model(self, request, obj, form, change):
        obj.save()
        set_metadata(obj, form.cleaned_data)


slot_admin.site.register(EasyPortlet, EasyPortletAdmin)
