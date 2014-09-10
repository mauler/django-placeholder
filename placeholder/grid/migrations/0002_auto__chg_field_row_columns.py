# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Row.columns'
        db.alter_column(u'grid_row', 'columns', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Row.columns'
        raise RuntimeError("Cannot reverse this migration. 'Row.columns' and its values cannot be restored.")

    models = {
        u'grid.column': {
            'Meta': {'object_name': 'Column'},
            'grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['grid.Grid']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'row': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'row_column_set'", 'null': 'True', 'to': u"orm['grid.Row']"}),
            'rows': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'grid.grid': {
            'Meta': {'object_name': 'Grid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'grid.row': {
            'Meta': {'object_name': 'Row'},
            'column': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'column_row_set'", 'to': u"orm['grid.Column']"}),
            'columns': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['grid']