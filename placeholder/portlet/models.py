from json import loads

from django.conf import settings
from django.db.models import signals
from django.db import models

from ..slot.models import Portlet


class EasyPortlet(Portlet):
    template_name = models.FilePathField(
        allow_folders=False,
        blank=True,
        path=settings.EASYPORTLET_TEMPLATES_PATH,
        recursive=True,
    )
    json_data = models.TextField()


def easyportlet_post_init(sender, instance, **kw):
    if instance.json_data:
        data = loads(instance.json_data)
        for k, v in data.items():
            setattr(instance, k, v)


signals.post_init.connect(easyportlet_post_init, sender=EasyPortlet)


class File(models.Model):
    portlet = models.ForeignKey("EasyPortlet")
    file = models.FileField(upload_to="portlets/files")


class Item(models.Model):
    portlet = models.ForeignKey("EasyPortlet")
    title = models.CharField(max_length=100)
    json_data = models.TextField()


class ItemFile(models.Model):
    item = models.ForeignKey("Item")
    file = models.FileField(upload_to="portlets/files")
