# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Portlet'
        db.create_table(u'slot_portlet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_slot.portlet_set', null=True, to=orm['contenttypes.ContentType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'slot', ['Portlet'])

        # Adding model 'Slot'
        db.create_table(u'slot_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'slot', ['Slot'])

        # Adding model 'SlotPortlet'
        db.create_table(u'slot_slotportlet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['slot.Slot'])),
            ('portlet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['slot.Portlet'])),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(default=2)),
        ))
        db.send_create_signal(u'slot', ['SlotPortlet'])

        # Adding unique constraint on 'SlotPortlet', fields ['slot', 'portlet']
        db.create_unique(u'slot_slotportlet', ['slot_id', 'portlet_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SlotPortlet', fields ['slot', 'portlet']
        db.delete_unique(u'slot_slotportlet', ['slot_id', 'portlet_id'])

        # Deleting model 'Portlet'
        db.delete_table(u'slot_portlet')

        # Deleting model 'Slot'
        db.delete_table(u'slot_slot')

        # Deleting model 'SlotPortlet'
        db.delete_table(u'slot_slotportlet')


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
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'portlet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Portlet']"}),
            'slot': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['slot.Slot']"})
        }
    }

    complete_apps = ['slot']