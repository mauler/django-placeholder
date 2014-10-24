#-*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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
