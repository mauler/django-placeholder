__version__ = "0.0.1"

import threading

from django.contrib import admin
from django.utils.encoding import iri_to_uri
from django import forms


world = threading.local()


def register(modeladmin, placeholder, key=None):
    if key is None:
        key = placeholder.__name__.replace("Placeholder", "")
    modeladmin.registred_placeholders[key] = placeholder


class PlaceholderAdmin(admin.ModelAdmin):
    registred_placeholders = {}

    def get_form(self, request, obj=None, **kwargs):
        k = 'placeholder_admin'
        if k in request.GET:
            k = request.GET[k]
            ph = self.registred_placeholders.get(k)
            if ph:

                if getattr(ph, 'nullform'):

                    class NullForm(forms.ModelForm):
                        class Meta:
                            fields = []
                            model = self.model

                    return NullForm

                if getattr(ph, "form", None) is not None:
                    return ph.form

        return super(PlaceholderAdmin, self).get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        k = 'placeholder_admin'
        if k in request.GET:
            k = request.GET[k]
            ph = self.registred_placeholders.get(k)
            if ph is not None and getattr(ph, "fieldsets", None) is not None:
                return ph.fieldsets

        return super(PlaceholderAdmin, self).get_fieldsets(request, obj)

    def get_inline_instances(self, request, obj=None):
        k = 'placeholder_admin'
        if k in request.GET:
            k = request.GET[k]
            ph = self.registred_placeholders.get(k)
            if ph is not None and getattr(ph, "fieldsets", None) is not None:
                return [
                    inline(self.model, self.admin_site)
                    for inline in ph.inlines]

        return super(PlaceholderAdmin, self).get_inline_instances(request, obj)

    def response_change(self, request, obj):
        response = super(PlaceholderAdmin, self).response_change(request, obj)
        if '_popup' in request.POST and 'pop=1' not in response['Location']:
            response['Location'] = iri_to_uri(response['Location'] + '?pop=1')
        return response
