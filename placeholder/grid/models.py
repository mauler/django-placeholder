from django.db.models import signals
from django.db import models


class Row(models.Model):
    column = models.ForeignKey(
        "Column",
        related_name="column_row_set",
    )
    columns = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        l = []
        for col in self.row_column_set.all():
            print col
            l.append("[%d,%d]" % (col.size, col.rows))
        name = "".join(l) or '[]'

        return "%s R %s" % (self.column, name)


def row_post_save(sender, instance, created, *args, **kwargs):
    col_count = instance.row_column_set.count()
    if col_count > instance.columns:
        instance.row_column_set.all()[instance.columns:].delete()
    elif col_count < instance.columns:
        for i in range(col_count, instance.columns):
            size = 12 / instance.columns
            instance.row_column_set.create(size=size)


signals.post_save.connect(row_post_save, sender=Row)


class Column(models.Model):
    grid = models.ForeignKey("Grid", blank=True, null=True)
    row = models.ForeignKey(
        "Row", blank=True, null=True,
        related_name="row_column_set",
    )
    size = models.PositiveIntegerField()
    rows = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        if self.grid:
            qs = self.grid.column_set.all()
        else:
            qs = self.row.row_column_set.all()

        l = []
        for column in qs:
            if column == self:
                l.append('[@%d,%d]' % (self.size, self.rows))
            else:
                l.append('[%d,%d]' % (column.size, column.rows))
        if self.grid:
            return "%s %s" % (self.grid.name, "".join(l))
        return "".join(l)


def column_post_save(sender, instance, created, *args, **kwargs):
    row_count = instance.column_row_set.count()
    if row_count > instance.rows:
        instance.column_row_set.all()[instance.rows:].delete()
    elif row_count < instance.rows:
        for i in range(row_count, instance.rows):
            instance.column_row_set.create()


signals.post_save.connect(column_post_save, sender=Column)


class Grid(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name
        if self.column_set.exists():
            name = ""
            for col in self.column_set.all():
                name += '[%s]' % col
            return "%s %s" % (self.name, name)
        return self.name
