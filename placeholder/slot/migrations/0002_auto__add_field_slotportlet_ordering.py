# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SlotPortlet.ordering'
        db.add_column(u'slot_slotportlet', 'ordering',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=999),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SlotPortlet.ordering'
        db.delete_column(u'slot_slotportlet', 'ordering')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'slot.portlet': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Portlet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_slot.portlet_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'slot.slot': {
            'Meta': {'object_name': 'Slot'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {'unique': 'True', 'db_index': 'True'}),
            'portlets': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['slot.Portlet']", 'through': u"orm['slot.SlotPortlet']", 'symmetrical': 'False'})
        },
        u'slot.slotportlet': {
            'Meta': {'ordering': "('id', 'ordering')", 'object_name': 'SlotPortlet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '999'}),
            'portlet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Portlet']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Slot']"})
        }
    }

    complete_apps = ['slot']