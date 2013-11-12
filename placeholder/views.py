#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db.models.loading import get_model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def placeholder_save(request):
    model_class = get_model(request.POST['app_label'],
                            request.POST['model_name'])
    obj = model_class.objects.get(pk=request.POST['model_pk'])
    setattr(obj, request.POST['model_attribute'], request.POST['value'])
    obj.save()
    return HttpResponse()
