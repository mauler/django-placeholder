from django.contrib.admin import ModelAdmin, site, StackedInline

from .models import Grid, Column, Row


class GridColumnInline(StackedInline):
    extra = 0
    model = Column
    fields = ("grid", "size", "rows", )


class GridAdmin(ModelAdmin):
    inlines = (GridColumnInline, )


site.register(Grid, GridAdmin)


class RowInline(StackedInline):
    extra = 0
    model = Row


class ColumnAdmin(ModelAdmin):
    inlines = (RowInline, )
    readonly_fields = ("grid", "row", )


site.register(Column, ColumnAdmin)


class ColumnInline(StackedInline):
    extra = 0
    model = Column
    fields = ("row", "size", "rows", )


class RowAdmin(ModelAdmin):
    inlines = (ColumnInline, )


site.register(Row, RowAdmin)
