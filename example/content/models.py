
from django.db import models

from placeholder.slot.models import Portlet


class RecipePortlet(Portlet):
    template_name = 'portlet/recipe.html'
    body = models.TextField()
    image = models.ImageField(upload_to='images')


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='images')
    position = models.IntegerField(default=1)

    class Meta:
        ordering = ('position', )

    def __unicode__(self):
        return self.title
