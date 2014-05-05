# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SecretSanta'
        db.create_table(u'secret_santa_secretsanta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
            ('enrollment_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('enrollment_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('lottery_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('lottery_done', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price_class', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'secret_santa', ['SecretSanta'])

        # Adding model 'Participant'
        db.create_table(u'secret_santa_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('secret_santa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['secret_santa.SecretSanta'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'secret_santa', ['Participant'])

        # Adding model 'Couple'
        db.create_table(u'secret_santa_couple', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('secret_santa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['secret_santa.SecretSanta'], null=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['secret_santa.Participant'])),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['secret_santa.Participant'])),
        ))
        db.send_create_signal(u'secret_santa', ['Couple'])


    def backwards(self, orm):
        # Deleting model 'SecretSanta'
        db.delete_table(u'secret_santa_secretsanta')

        # Deleting model 'Participant'
        db.delete_table(u'secret_santa_participant')

        # Deleting model 'Couple'
        db.delete_table(u'secret_santa_couple')


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
        u'secret_santa.couple': {
            'Meta': {'object_name': 'Couple'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receiver'", 'to': u"orm['secret_santa.Participant']"}),
            'secret_santa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['secret_santa.SecretSanta']", 'null': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['secret_santa.Participant']"})
        },
        u'secret_santa.participant': {
            'Meta': {'ordering': "['secret_santa', 'user__username']", 'object_name': 'Participant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret_santa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['secret_santa.SecretSanta']", 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'secret_santa.secretsanta': {
            'Meta': {'ordering': "['-year']", 'object_name': 'SecretSanta'},
            'enrollment_end': ('django.db.models.fields.DateTimeField', [], {}),
            'enrollment_start': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lottery_date': ('django.db.models.fields.DateTimeField', [], {}),
            'lottery_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_class': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
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

    complete_apps = ['secret_santa']