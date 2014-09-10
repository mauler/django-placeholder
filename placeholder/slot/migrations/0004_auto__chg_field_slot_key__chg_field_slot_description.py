# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Slot.key'
        db.alter_column(u'slot_slot', 'key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024))

        # Changing field 'Slot.description'
        db.alter_column(u'slot_slot', 'description', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Slot.key'
        db.alter_column(u'slot_slot', 'key', self.gf('django.db.models.fields.TextField')(unique=True))

        # Changing field 'Slot.description'
        db.alter_column(u'slot_slot', 'description', self.gf('django.db.models.fields.TextField')())

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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'db_index': 'True'}),
            'portlets': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['slot.Portlet']", 'through': u"orm['slot.SlotPortlet']", 'symmetrical': 'False'})
        },
        u'slot.slotportlet': {
            'Meta': {'ordering': "('ordering',)", 'unique_together': "(('slot', 'portlet'),)", 'object_name': 'SlotPortlet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '5'}),
            'portlet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Portlet']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Slot']"})
        }
    }

    complete_apps = ['slot']