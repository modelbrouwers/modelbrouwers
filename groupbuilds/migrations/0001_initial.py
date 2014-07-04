# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupBuild'
        db.create_table(u'groupbuilds_groupbuild', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('theme', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum_tools.ForumCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=92)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('users_can_vote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('upvotes', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('downvotes', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('rules', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rules_topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('homepage_topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('introduction_topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupbuilds_applied', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reason_denied', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'groupbuilds', ['GroupBuild'])

        # Adding M2M table for field admins on 'GroupBuild'
        m2m_table_name = db.shorten_name(u'groupbuilds_groupbuild_admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groupbuild', models.ForeignKey(orm[u'groupbuilds.groupbuild'], null=False)),
            ('user', models.ForeignKey(orm[u'users.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['groupbuild_id', 'user_id'])

        # Adding model 'Participant'
        db.create_table(u'groupbuilds_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('groupbuild', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupbuilds.GroupBuild'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gb_participants', to=orm['users.User'])),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('topic_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('points', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'groupbuilds', ['Participant'])


    def backwards(self, orm):
        # Deleting model 'GroupBuild'
        db.delete_table(u'groupbuilds_groupbuild')

        # Removing M2M table for field admins on 'GroupBuild'
        db.delete_table(db.shorten_name(u'groupbuilds_groupbuild_admins'))

        # Deleting model 'Participant'
        db.delete_table(u'groupbuilds_participant')


    models = {
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
        u'forum_tools.forumcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ForumCategory'},
            'forum_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'groupbuilds.groupbuild': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'GroupBuild'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admin_groupbuilds'", 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupbuilds_applied'", 'to': u"orm['users.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['forum_tools.ForumCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'downvotes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '92'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'forum_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'homepage_topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction_topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groupbuilds'", 'to': u"orm['users.User']", 'through': u"orm['groupbuilds.Participant']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'reason_denied': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rules': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rules_topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upvotes': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'users_can_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'groupbuilds.participant': {
            'Meta': {'object_name': 'Participant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'groupbuild': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['groupbuilds.GroupBuild']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'points': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'topic_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gb_participants'", 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'forumuser_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['groupbuilds']