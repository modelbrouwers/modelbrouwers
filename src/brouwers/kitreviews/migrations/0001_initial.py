# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table(u'kitreviews_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal(u'kitreviews', ['Brand'])

        # Adding model 'Scale'
        db.create_table(u'kitreviews_scale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scale', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'kitreviews', ['Scale'])

        # Adding model 'Category'
        db.create_table(u'kitreviews_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'kitreviews', ['Category'])

        # Adding model 'ModelKit'
        db.create_table(u'kitreviews_modelkit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.Brand'])),
            ('kit_number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('scale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.Scale'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.Category'], null=True)),
            ('difficulty', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('box_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('submitted_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kitreviews', ['ModelKit'])

        # Adding M2M table for field duplicates on 'ModelKit'
        m2m_table_name = db.shorten_name(u'kitreviews_modelkit_duplicates')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_modelkit', models.ForeignKey(orm[u'kitreviews.modelkit'], null=False)),
            ('to_modelkit', models.ForeignKey(orm[u'kitreviews.modelkit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_modelkit_id', 'to_modelkit_id'])

        # Adding model 'KitReview'
        db.create_table(u'kitreviews_kitreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model_kit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.ModelKit'])),
            ('raw_text', self.gf('django.db.models.fields.TextField')()),
            ('html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('positive_points', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('negative_points', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=50)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Album'], null=True, blank=True)),
            ('topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('external_topic_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('show_real_name', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('submitted_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_edited_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'kitreviews', ['KitReview'])

        # Adding model 'KitReviewVote'
        db.create_table(u'kitreviews_kitreviewvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kit_review', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitreviews.KitReview'])),
            ('vote', self.gf('django.db.models.fields.CharField')(max_length=1, db_index=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'kitreviews', ['KitReviewVote'])

        # Adding unique constraint on 'KitReviewVote', fields ['kit_review', 'voter']
        db.create_unique(u'kitreviews_kitreviewvote', ['kit_review_id', 'voter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'KitReviewVote', fields ['kit_review', 'voter']
        db.delete_unique(u'kitreviews_kitreviewvote', ['kit_review_id', 'voter_id'])

        # Deleting model 'Brand'
        db.delete_table(u'kitreviews_brand')

        # Deleting model 'Scale'
        db.delete_table(u'kitreviews_scale')

        # Deleting model 'Category'
        db.delete_table(u'kitreviews_category')

        # Deleting model 'ModelKit'
        db.delete_table(u'kitreviews_modelkit')

        # Removing M2M table for field duplicates on 'ModelKit'
        db.delete_table(db.shorten_name(u'kitreviews_modelkit_duplicates'))

        # Deleting model 'KitReview'
        db.delete_table(u'kitreviews_kitreview')

        # Deleting model 'KitReviewVote'
        db.delete_table(u'kitreviews_kitreviewvote')


    models = {
        u'albums.album': {
            'Meta': {'ordering': "('order', 'title')", 'unique_together': "(('user', 'title'),)", 'object_name': 'Album'},
            'build_report': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['albums.Category']", 'null': 'True', 'blank': 'True'}),
            'clean_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': "'256'", 'blank': 'True'}),
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cover'", 'null': 'True', 'to': u"orm['albums.Photo']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_upload': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'album 27-12-2014'", 'max_length': "'256'", 'db_index': 'True'}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'writable_to': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
        },
        u'albums.category': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'on_frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'albums.photo': {
            'Meta': {'ordering': "['album', 'order', 'pk']", 'object_name': 'Photo'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['albums.Album']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'}),
            'trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kitreviews.brand': {
            'Meta': {'ordering': "['name']", 'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        u'kitreviews.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'kitreviews.kitreview': {
            'Meta': {'object_name': 'KitReview'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['albums.Album']", 'null': 'True', 'blank': 'True'}),
            'external_topic_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_edited_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'model_kit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitreviews.ModelKit']"}),
            'negative_points': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'positive_points': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '50'}),
            'raw_text': ('django.db.models.fields.TextField', [], {}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'show_real_name': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'kitreviews.kitreviewvote': {
            'Meta': {'unique_together': "(('kit_review', 'voter'),)", 'object_name': 'KitReviewVote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_review': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitreviews.KitReview']"}),
            'vote': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_index': 'True'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'kitreviews.modelkit': {
            'Meta': {'object_name': 'ModelKit'},
            'box_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitreviews.Brand']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitreviews.Category']", 'null': 'True'}),
            'difficulty': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'duplicates_rel_+'", 'null': 'True', 'to': u"orm['kitreviews.ModelKit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'scale': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitreviews.Scale']"}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'kitreviews.scale': {
            'Meta': {'ordering': "['scale']", 'object_name': 'Scale'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scale': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True'})
        },
        u'users.user': {
            'Meta': {'ordering': "['username_clean']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'forumuser_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'username_clean': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['kitreviews']