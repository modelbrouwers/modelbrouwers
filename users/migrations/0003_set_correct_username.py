# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        """
        Replace the underscored usernames with the usernames in the UserProfile.
        """
        for profile in orm['general.UserProfile'].objects.select_related('user').all():
            user = profile.user
            user.username = profile.forum_nickname
            user.save()

    def backwards(self, orm):
        """
        Replace spaces in the usernames with underscores
        """
        for user in orm.User.objects.all():
            user.username = user.username.replace(' ', '_')
            user.save()

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
        u'awards.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'banning.ban': {
            'Meta': {'object_name': 'Ban'},
            'automatic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reason_internal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'general.announcement': {
            'Meta': {'ordering': "['-from_date']", 'object_name': 'Announcement'},
            'from_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'general.passwordreset': {
            'Meta': {'ordering': "('expire',)", 'unique_together': "(('user', 'h'),)", 'object_name': 'PasswordReset'},
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'h': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'general.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'general.redirect': {
            'Meta': {'ordering': "('path_from',)", 'object_name': 'Redirect'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path_from': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'path_to': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'general.registrationattempt': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'RegistrationAttempt'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ban': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['banning.Ban']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['general.RegistrationQuestion']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type_of_visitor': ('django.db.models.fields.CharField', [], {'default': "u'normal user'", 'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'_not_filled_in_'", 'max_length': '512', 'db_index': 'True'})
        },
        u'general.registrationquestion': {
            'Meta': {'object_name': 'RegistrationQuestion'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['general.QuestionAnswer']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_use': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'general.softwareversion': {
            'Meta': {'ordering': "('-state', '-major', '-minor', '-detail')", 'object_name': 'SoftwareVersion'},
            'changelog': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'minor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'v'", 'max_length': '1'})
        },
        u'general.userprofile': {
            'Meta': {'ordering': "['forum_nickname']", 'object_name': 'UserProfile'},
            'allow_sharing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'categories_voted': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['awards.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'exclude_from_nomination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forum_nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_vote': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2010, 1, 1, 0, 0)'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'preference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'refuse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secret_santa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'unique': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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

    complete_apps = ['general', 'users']
    symmetrical = True
