from django.contrib import admin

from placeholder.slot import admin as slot_admin

from .models import Post, RecipePortlet


slot_admin.site.register(RecipePortlet)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "position", )
    list_editable = ("position", )


admin.site.register(Post, PostAdmin)
