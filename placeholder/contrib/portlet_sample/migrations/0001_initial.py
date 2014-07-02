# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CTPortlet'
        db.create_table(u'portlet_sample_ctportlet', (
            (u'portlet_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['slot.Portlet'], unique=True, primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('template_name', self.gf('django.db.models.fields.CharField')(default='portlet/default.html', max_length=100)),
        ))
        db.send_create_signal(u'portlet_sample', ['CTPortlet'])


    def backwards(self, orm):
        # Deleting model 'CTPortlet'
        db.delete_table(u'portlet_sample_ctportlet')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'portlet_sample.ctportlet': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'CTPortlet', '_ormbases': [u'slot.Portlet']},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'portlet_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slot.Portlet']", 'unique': 'True', 'primary_key': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'default': "'portlet/default.html'", 'max_length': '100'})
        },
        u'slot.portlet': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'Portlet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_slot.portlet_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['portlet_sample']
