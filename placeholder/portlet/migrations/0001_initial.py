# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EasyPortlet'
        db.create_table(u'portlet_easyportlet', (
            (u'portlet_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['slot.Portlet'], unique=True, primary_key=True)),
            ('template_name', self.gf('django.db.models.fields.FilePathField')(path='content/templates/portlet', max_length=100, recursive=True, blank=True)),
            ('json_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'portlet', ['EasyPortlet'])

        # Adding model 'File'
        db.create_table(u'portlet_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('portlet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portlet.EasyPortlet'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'portlet', ['File'])

        # Adding model 'Item'
        db.create_table(u'portlet_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('portlet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portlet.EasyPortlet'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('json_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'portlet', ['Item'])

        # Adding model 'ItemFile'
        db.create_table(u'portlet_itemfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['portlet.Item'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'portlet', ['ItemFile'])


    def backwards(self, orm):
        # Deleting model 'EasyPortlet'
        db.delete_table(u'portlet_easyportlet')

        # Deleting model 'File'
        db.delete_table(u'portlet_file')

        # Deleting model 'Item'
        db.delete_table(u'portlet_item')

        # Deleting model 'ItemFile'
        db.delete_table(u'portlet_itemfile')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'portlet.easyportlet': {
            'Meta': {'ordering': "('title',)", 'object_name': 'EasyPortlet', '_ormbases': [u'slot.Portlet']},
            'json_data': ('django.db.models.fields.TextField', [], {}),
            u'portlet_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slot.Portlet']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.FilePathField', [], {'path': "'content/templates/portlet'", 'max_length': '100', 'recursive': 'True', 'blank': 'True'})
        },
        u'portlet.file': {
            'Meta': {'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portlet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portlet.EasyPortlet']"})
        },
        u'portlet.item': {
            'Meta': {'object_name': 'Item'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json_data': ('django.db.models.fields.TextField', [], {}),
            'portlet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portlet.EasyPortlet']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'portlet.itemfile': {
            'Meta': {'object_name': 'ItemFile'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['portlet.Item']"})
        },
        u'slot.portlet': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Portlet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_slot.portlet_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['portlet']