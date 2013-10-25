# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table('kitreviews_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('kitreviews', ['Brand'])

        # Adding model 'Scale'
        db.create_table('kitreviews_scale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scale', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
        ))
        db.send_create_signal('kitreviews', ['Scale'])

        # Adding model 'ModelKit'
        db.create_table('kitreviews_modelkit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.Brand'])),
            ('kit_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.Scale'])),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submitted_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('kitreviews', ['ModelKit'])

        # Adding M2M table for field duplicates on 'ModelKit'
        db.create_table('kitreviews_modelkit_duplicates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_modelkit', models.ForeignKey(orm['kitreviews.modelkit'], null=False)),
            ('to_modelkit', models.ForeignKey(orm['kitreviews.modelkit'], null=False))
        ))
        db.create_unique('kitreviews_modelkit_duplicates', ['from_modelkit_id', 'to_modelkit_id'])

        # Adding model 'KitReview'
        db.create_table('kitreviews_kitreview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_kit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.ModelKit'])),
            ('raw_text', self.gf('django.db.models.fields.TextField')()),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=50)),
            ('difficulty', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Album'], null=True, blank=True)),
            ('topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('external_topic_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('show_real_name', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submitted_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edited_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('kitreviews', ['KitReview'])

        # Adding model 'KitReviewVote'
        db.create_table('kitreviews_kitreviewvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kit_review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.KitReview'])),
            ('vote', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('kitreviews', ['KitReviewVote'])

        # Adding unique constraint on 'KitReviewVote', fields ['kit_review', 'voter']
        db.create_unique('kitreviews_kitreviewvote', ['kit_review_id', 'voter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'KitReviewVote', fields ['kit_review', 'voter']
        db.delete_unique('kitreviews_kitreviewvote', ['kit_review_id', 'voter_id'])

        # Deleting model 'Brand'
        db.delete_table('kitreviews_brand')

        # Deleting model 'Scale'
        db.delete_table('kitreviews_scale')

        # Deleting model 'ModelKit'
        db.delete_table('kitreviews_modelkit')

        # Removing M2M table for field duplicates on 'ModelKit'
        db.delete_table('kitreviews_modelkit_duplicates')

        # Deleting model 'KitReview'
        db.delete_table('kitreviews_kitreview')

        # Deleting model 'KitReviewVote'
        db.delete_table('kitreviews_kitreviewvote')


    models = {
        'albums.album': {
            'Meta': {'ordering': "('order', 'title')", 'unique_together': "(('user', 'title'),)", 'object_name': 'Album'},
            'build_report': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['albums.Category']", 'null': 'True', 'blank': 'True'}),
            'clean_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'256'", 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover'", 'null': 'True', 'to': "orm['albums.Photo']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_upload': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'album 05-06-2013'", 'max_length': "'256'", 'db_index': 'True'}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'writable_to': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
        },
        'albums.category': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'on_frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        'albums.photo': {
            'Meta': {'ordering': "['album', 'order', 'pk']", 'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['albums.Album']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'kitreviews.brand': {
            'Meta': {'ordering': "['name']", 'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'kitreviews.kitreview': {
            'Meta': {'object_name': 'KitReview'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['albums.Album']", 'null': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'external_topic_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'model_kit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kitreviews.ModelKit']"}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '50'}),
            'raw_text': ('django.db.models.fields.TextField', [], {}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'show_real_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'kitreviews.kitreviewvote': {
            'Meta': {'unique_together': "(('kit_review', 'voter'),)", 'object_name': 'KitReviewVote'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_review': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kitreviews.KitReview']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'kitreviews.modelkit': {
            'Meta': {'object_name': 'ModelKit'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kitreviews.Brand']"}),
            'duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'duplicates_rel_+'", 'null': 'True', 'to': "orm['kitreviews.ModelKit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['kitreviews.Scale']"}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'kitreviews.scale': {
            'Meta': {'ordering': "['scale']", 'object_name': 'Scale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scale': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['kitreviews']