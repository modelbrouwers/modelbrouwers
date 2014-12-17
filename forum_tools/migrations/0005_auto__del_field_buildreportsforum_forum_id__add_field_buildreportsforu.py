# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        """
        The literal field changed from forum_id to forum, but the column name
        stays the same. So, do nothing.
        """
        pass


    def backwards(self, orm):
        """See comment in ``forward``. """
        pass


    models = {
        u'forum_tools.buildreportsforum': {
            'Meta': {'ordering': "['forum']", 'object_name': 'BuildReportsForum'},
            'forum': ('forum_tools.fields.ForumToolsIDField', [], {'type': "'forum'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'forum_tools.forum': {
            'Meta': {'ordering': "['forum_name']", 'object_name': 'Forum', 'db_table': "'phpbb_forums'", 'managed': 'False'},
            'forum_desc': ('django.db.models.fields.TextField', [], {}),
            'forum_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'forum_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'forum_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'forum_topics': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'child'", 'to': u"orm['forum_tools.Forum']"})
        },
        u'forum_tools.forumcategory': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ForumCategory'},
            'forum': ('forum_tools.fields.ForumToolsIDField', [], {'null': 'True', 'type': "'forum'", 'blank': 'True'}),
            'icon_class': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
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
        },
        u'forum_tools.topic': {
            'Meta': {'ordering': "['topic_id']", 'object_name': 'Topic', 'db_table': "'phpbb_topics'", 'managed': 'False'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['forum_tools.Forum']"}),
            'topic_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'topic_title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['forum_tools']
