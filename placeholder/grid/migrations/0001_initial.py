# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Row'
        db.create_table(u'grid_row', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('column', self.gf('django.db.models.fields.related.ForeignKey')(related_name='column_row_set', to=orm['grid.Column'])),
            ('columns', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
        ))
        db.send_create_signal(u'grid', ['Row'])

        # Adding model 'Column'
        db.create_table(u'grid_column', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['grid.Grid'], null=True, blank=True)),
            ('row', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='row_column_set', null=True, to=orm['grid.Row'])),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rows', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'grid', ['Column'])

        # Adding model 'Grid'
        db.create_table(u'grid_grid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'grid', ['Grid'])


    def backwards(self, orm):
        # Deleting model 'Row'
        db.delete_table(u'grid_row')

        # Deleting model 'Column'
        db.delete_table(u'grid_column')

        # Deleting model 'Grid'
        db.delete_table(u'grid_grid')


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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'db_index': 'True'})
        },
        u'grid.row': {
            'Meta': {'object_name': 'Row'},
            'column': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'column_row_set'", 'to': u"orm['grid.Column']"}),
            'columns': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['grid']