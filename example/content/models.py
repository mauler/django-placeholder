from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='images')

    class Meta:
        ordering = ('-id', )

    def __unicode__(self):
        return self.title
