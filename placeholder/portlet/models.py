from django.conf import settings
from django.db.models import signals
from django.db import models

from ..slot.models import Portlet
from .utils import apply_metadata


class EasyPortlet(Portlet):
    template_name = models.FilePathField(
        allow_folders=False,
        blank=True,
        path=settings.EASYPORTLET_TEMPLATES_PATH,
        recursive=True,
    )
    json_data = models.TextField()

    def get_template_name(self):
        path = self._meta.get_field('template_name').path
        return 'portlets' + self.template_name.replace(path, '', 1)


def json_data_post_init(sender, instance, **kw):
    apply_metadata(instance)


signals.post_init.connect(json_data_post_init, sender=EasyPortlet)


class File(models.Model):
    portlet = models.ForeignKey("EasyPortlet")
    fieldname = models.CharField(max_length=50)
    file = models.FileField(upload_to="portlets/files")


class Item(models.Model):
    portlet = models.ForeignKey("EasyPortlet")
    title = models.CharField(max_length=100)
    json_data = models.TextField()
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("portlet", "position", "title", )

    def __unicode__(self):
        return self.title


signals.post_init.connect(json_data_post_init, sender=Item)


class ItemFile(models.Model):
    item = models.ForeignKey("Item", related_name="file_set")
    fieldname = models.CharField(max_length=50)
    file = models.FileField(upload_to="portlets/files")
