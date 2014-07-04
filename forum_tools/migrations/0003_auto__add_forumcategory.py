# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ForumCategory'
        db.create_table(u'forum_tools_forumcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('forum_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'forum_tools', ['ForumCategory'])


    def backwards(self, orm):
        # Deleting model 'ForumCategory'
        db.delete_table(u'forum_tools_forumcategory')


    models = {
        u'forum_tools.buildreportsforum': {
            'Meta': {'ordering': "['forum_id']", 'object_name': 'BuildReportsForum'},
            'forum_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'forum_tools.forum': {
            'Meta': {'ordering': "['forum_name']", 'object_name': 'Forum', 'db_table': "'phpbb_forums'", 'managed': 'False'},
            'forum_desc': ('django.db.models.fields.TextField', [], {}),
            'forum_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'forum_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'forum_posts': ('django.db.models.fields.IntegerField', [], {}),
            'forum_topics': ('django.db.models.fields.IntegerField', [], {}),
            'left': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'right_of'", 'unique': 'True', 'to': u"orm['forum_tools.Forum']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child'", 'to': u"orm['forum_tools.Forum']"}),
            'right': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'left_of'", 'unique': 'True', 'to': u"orm['forum_tools.Forum']"})
        },
        u'forum_tools.forumcategory': {
            'Meta': {'object_name': 'ForumCategory'},
            'forum_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'forum_tools.forumlinkbase': {
            'Meta': {'object_name': 'ForumLinkBase'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'to_date': ('django.db.models.fields.DateField', [], {})
        },
        u'forum_tools.forumlinksynced': {
            'Meta': {'object_name': 'ForumLinkSynced'},
            'base': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['forum_tools.ForumLinkBase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'forum_tools.forumpostcountrestriction': {
            'Meta': {'ordering': "['forum']", 'object_name': 'ForumPostCountRestriction'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['forum_tools.Forum']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_posts': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'posting_level': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'forum_tools.forumuser': {
            'Meta': {'ordering': "('username',)", 'object_name': 'ForumUser', 'db_table': "u'phpbb_users'", 'managed': 'False'},
            'user_actkey': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_email_hash': ('django.db.models.fields.BigIntegerField', [], {'default': '0', 'db_column': "'user_email_hash'"}),
            'user_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'user_interests': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_occ': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_posts': ('django.db.models.fields.IntegerField', [], {}),
            'user_sig': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username_clean': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'forum_tools.report': {
            'Meta': {'object_name': 'Report', 'db_table': "u'phpbb_reports'", 'managed': 'False'},
            'report_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'report_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'report_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report_time_int': ('django.db.models.fields.IntegerField', [], {'db_column': "'report_time'"})
        }
    }

    complete_apps = ['forum_tools']