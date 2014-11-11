#-*- coding:utf-8 -*-

from json import loads, dumps

from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import get_model_image_upload_form


@login_required
def placeholder_upload(request):
    valid_user = request.user.is_authenticated() and request.user.is_staff
    if valid_user:
        model_class = get_model(request.POST['app_label'],
                                request.POST['model_name'])
        obj = model_class.objects.get(pk=request.POST['model_pk'])
        perm = obj._meta.get_change_permission()
        if perm:
            field = request.POST['model_field']
            form_class = get_model_image_upload_form(model_class, field)
            form = form_class(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form.save()
                return HttpResponse("true")
            else:
                return HttpResponse(dumps(form.errors))

    return HttpResponse("false")


@csrf_exempt
@login_required
def multiedit_save(request):
    valid_user = request.user.is_authenticated() and request.user.is_staff
    if valid_user:
        data = loads(request.POST['data'])

        for app_label, app_data in data.items():
            for model_name, model_data in app_data.items():
                model_class = get_model(app_label, model_name)
                for pk, changes in model_data.items():
                    obj = model_class.objects.get(pk=pk)
                    perm = obj._meta.get_change_permission()
                    if perm:
                        for attr, value in changes.items():
                            setattr(obj, attr, value)
                        obj.save(update_fields=changes.keys())

    return HttpResponse()


@csrf_exempt
@login_required
def placeholder_save(request):
    valid_user = request.user.is_authenticated() and request.user.is_staff
    if valid_user:
        model_class = get_model(request.POST['app_label'],
                                request.POST['model_name'])
        obj = model_class.objects.get(pk=request.POST['model_pk'])
        perm = obj._meta.get_change_permission()
        if perm:
            field = request.POST['model_field']
            setattr(obj, field, request.POST['value'])
            obj.save(update_fields=[field])

    return HttpResponse()
