# coding: utf-8

from __future__ import unicode_literals

from django.template.loader import get_template
from django.template import Context
from django.test import TestCase

from .models import Grid


class GridTestCase(TestCase):

    def setUp(self):
        self.grid = grid = Grid.objects.create()
        grid.column_set.create(size=6)
        cola = grid.column_set.create(size=6)
        cola.column_row_set.create()
        cola.column_row_set.create()

    def test_render(self):
        template = get_template("grid/grid.html")
        rendered = template.render(Context({'grid': self.grid}))
        print rendered
