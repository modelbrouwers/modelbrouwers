# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'albums_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('on_frontpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'albums', ['Category'])

        # Adding model 'Album'
        db.create_table(u'albums_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='album 27-12-2014', max_length='256', db_index=True)),
            ('clean_title', self.gf('django.db.models.fields.CharField')(default='', max_length='256', blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['albums.Category'], null=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cover', null=True, to=orm['albums.Photo'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('last_upload', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0), db_index=True)),
            ('views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, db_index=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('build_report', self.gf('django.db.models.fields.URLField')(max_length=500, blank=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('writable_to', self.gf('django.db.models.fields.CharField')(default='u', max_length=1)),
            ('trash', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'albums', ['Album'])

        # Adding unique constraint on 'Album', fields ['user', 'title']
        db.create_unique(u'albums_album', ['user_id', 'title'])

        # Adding model 'AlbumGroup'
        db.create_table(u'albums_albumgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Album'], unique=True)),
        ))
        db.send_create_signal(u'albums', ['AlbumGroup'])

        # Adding M2M table for field users on 'AlbumGroup'
        m2m_table_name = db.shorten_name(u'albums_albumgroup_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('albumgroup', models.ForeignKey(orm[u'albums.albumgroup'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['albumgroup_id', 'user_id'])

        # Adding model 'Photo'
        db.create_table(u'albums_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Album'])),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, null=True, db_index=True, blank=True)),
            ('trash', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'albums', ['Photo'])

        # Adding model 'Preferences'
        db.create_table(u'albums_preferences', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], unique=True)),
            ('default_img_size', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('default_uploader', self.gf('django.db.models.fields.CharField')(default='F', max_length=1)),
            ('auto_start_uploading', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_direct_link', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('apply_admin_permissions', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('collapse_sidebar', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hide_sidebar', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sidebar_bg_color', self.gf('django.db.models.fields.CharField')(default='black', max_length=7, blank=True)),
            ('sidebar_transparent', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text_color', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
        ))
        db.send_create_signal(u'albums', ['Preferences'])

        # Adding model 'AlbumDownload'
        db.create_table(u'albums_albumdownload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Album'])),
            ('downloader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('failed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'albums', ['AlbumDownload'])


    def backwards(self, orm):
        # Removing unique constraint on 'Album', fields ['user', 'title']
        db.delete_unique(u'albums_album', ['user_id', 'title'])

        # Deleting model 'Category'
        db.delete_table(u'albums_category')

        # Deleting model 'Album'
        db.delete_table(u'albums_album')

        # Deleting model 'AlbumGroup'
        db.delete_table(u'albums_albumgroup')

        # Removing M2M table for field users on 'AlbumGroup'
        db.delete_table(db.shorten_name(u'albums_albumgroup_users'))

        # Deleting model 'Photo'
        db.delete_table(u'albums_photo')

        # Deleting model 'Preferences'
        db.delete_table(u'albums_preferences')

        # Deleting model 'AlbumDownload'
        db.delete_table(u'albums_albumdownload')


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
        u'albums.albumdownload': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'AlbumDownload'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['albums.Album']"}),
            'downloader': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'failed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'albums.albumgroup': {
            'Meta': {'ordering': "('album',)", 'object_name': 'AlbumGroup'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['albums.Album']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'})
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
        u'albums.preferences': {
            'Meta': {'ordering': "('user',)", 'object_name': 'Preferences'},
            'apply_admin_permissions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_start_uploading': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'collapse_sidebar': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'default_img_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'default_uploader': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'hide_sidebar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_direct_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sidebar_bg_color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '7', 'blank': 'True'}),
            'sidebar_transparent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'text_color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'unique': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'})
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

    complete_apps = ['albums']