from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "position", )
    list_editable = ("position", )


admin.site.register(Post, PostAdmin)
