# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Image.caption'
        db.add_column('core_image', 'caption', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Image.client'
        db.add_column('core_image', 'client', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)

        # Adding field 'Image.display'
        db.add_column('core_image', 'display', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Image.creation_time'
        db.add_column('core_image', 'creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2010, 12, 30, 4, 1, 44, 120004), blank=True), keep_default=False)

        # Adding field 'Image.edit_time'
        db.add_column('core_image', 'edit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2010, 12, 30, 4, 1, 51, 232446), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Image.caption'
        db.delete_column('core_image', 'caption')

        # Deleting field 'Image.client'
        db.delete_column('core_image', 'client')

        # Deleting field 'Image.display'
        db.delete_column('core_image', 'display')

        # Deleting field 'Image.creation_time'
        db.delete_column('core_image', 'creation_time')

        # Deleting field 'Image.edit_time'
        db.delete_column('core_image', 'edit_time')


    models = {
        'core.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'client': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'edit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']
