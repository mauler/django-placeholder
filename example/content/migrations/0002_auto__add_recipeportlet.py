# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RecipePortlet'
        db.create_table(u'content_recipeportlet', (
            (u'portlet_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['slot.Portlet'], unique=True, primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'content', ['RecipePortlet'])


    def backwards(self, orm):
        # Deleting model 'RecipePortlet'
        db.delete_table(u'content_recipeportlet')


    models = {
        u'content.post': {
            'Meta': {'ordering': "('position',)", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.recipeportlet': {
            'Meta': {'ordering': "('-id',)", 'object_name': 'RecipePortlet', '_ormbases': [u'slot.Portlet']},
            'body': ('django.db.models.fields.TextField', [], {}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'portlet_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['slot.Portlet']", 'unique': 'True', 'primary_key': 'True'})
        },
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
        }
    }

    complete_apps = ['content']