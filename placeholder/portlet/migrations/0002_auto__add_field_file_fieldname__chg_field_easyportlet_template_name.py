# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'File.fieldname'
        db.add_column(u'portlet_file', 'fieldname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


        # Changing field 'EasyPortlet.template_name'
        db.alter_column(u'portlet_easyportlet', 'template_name', self.gf('django.db.models.fields.FilePathField')(path='templates/portlets', max_length=100, recursive=True))

    def backwards(self, orm):
        # Deleting field 'File.fieldname'
        db.delete_column(u'portlet_file', 'fieldname')


        # Changing field 'EasyPortlet.template_name'
        db.alter_column(u'portlet_easyportlet', 'template_name', self.gf('django.db.models.fields.FilePathField')(path='content/templates/portlet', max_length=100, recursive=True))

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
            'template_name': ('django.db.models.fields.FilePathField', [], {'path': "'templates/portlets'", 'max_length': '100', 'recursive': 'True', 'blank': 'True'})
        },
        u'portlet.file': {
            'Meta': {'object_name': 'File'},
            'fieldname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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