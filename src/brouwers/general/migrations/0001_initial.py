# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('general_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('last_vote', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2010, 1, 1, 0, 0))),
            ('forum_nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('exclude_from_nomination', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('secret_santa', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('preference', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('refuse', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('general', ['UserProfile'])

        # Adding M2M table for field categories_voted on 'UserProfile'
        db.create_table('general_userprofile_categories_voted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['general.userprofile'], null=False)),
            ('category', models.ForeignKey(orm['awards.category'], null=False))
        ))
        db.create_unique('general_userprofile_categories_voted', ['userprofile_id', 'category_id'])

        # Adding model 'QuestionAnswer'
        db.create_table('general_questionanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('general', ['QuestionAnswer'])

        # Adding model 'RegistrationQuestion'
        db.create_table('general_registrationquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('in_use', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('general', ['RegistrationQuestion'])

        # Adding M2M table for field answers on 'RegistrationQuestion'
        db.create_table('general_registrationquestion_answers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registrationquestion', models.ForeignKey(orm['general.registrationquestion'], null=False)),
            ('questionanswer', models.ForeignKey(orm['general.questionanswer'], null=False))
        ))
        db.create_unique('general_registrationquestion_answers', ['registrationquestion_id', 'questionanswer_id'])

        # Adding model 'RegistrationAttempt'
        db.create_table('general_registrationattempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['general.RegistrationQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, db_index=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_of_visitor', self.gf('django.db.models.fields.CharField')(default=u'normal user', max_length=255)),
        ))
        db.send_create_signal('general', ['RegistrationAttempt'])

        # Adding model 'SoftwareVersion'
        db.create_table('general_softwareversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='v', max_length=1)),
            ('major', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('minor', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('detail', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('changelog', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('general', ['SoftwareVersion'])

        # Adding model 'PasswordReset'
        db.create_table('general_passwordreset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('h', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('expire', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('general', ['PasswordReset'])

        # Adding unique constraint on 'PasswordReset', fields ['user', 'h']
        db.create_unique('general_passwordreset', ['user_id', 'h'])

        # Adding model 'Redirect'
        db.create_table('general_redirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path_from', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('path_to', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('general', ['Redirect'])


    def backwards(self, orm):
        # Removing unique constraint on 'PasswordReset', fields ['user', 'h']
        db.delete_unique('general_passwordreset', ['user_id', 'h'])

        # Deleting model 'UserProfile'
        db.delete_table('general_userprofile')

        # Removing M2M table for field categories_voted on 'UserProfile'
        db.delete_table('general_userprofile_categories_voted')

        # Deleting model 'QuestionAnswer'
        db.delete_table('general_questionanswer')

        # Deleting model 'RegistrationQuestion'
        db.delete_table('general_registrationquestion')

        # Removing M2M table for field answers on 'RegistrationQuestion'
        db.delete_table('general_registrationquestion_answers')

        # Deleting model 'RegistrationAttempt'
        db.delete_table('general_registrationattempt')

        # Deleting model 'SoftwareVersion'
        db.delete_table('general_softwareversion')

        # Deleting model 'PasswordReset'
        db.delete_table('general_passwordreset')

        # Deleting model 'Redirect'
        db.delete_table('general_redirect')


    models = {
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
        'awards.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'general.passwordreset': {
            'Meta': {'ordering': "('expire',)", 'unique_together': "(('user', 'h'),)", 'object_name': 'PasswordReset'},
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'h': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'general.questionanswer': {
            'Meta': {'object_name': 'QuestionAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'general.redirect': {
            'Meta': {'ordering': "('path_from',)", 'object_name': 'Redirect'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path_from': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'path_to': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        'general.registrationattempt': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'RegistrationAttempt'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['general.RegistrationQuestion']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type_of_visitor': ('django.db.models.fields.CharField', [], {'default': "u'normal user'", 'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'general.registrationquestion': {
            'Meta': {'object_name': 'RegistrationQuestion'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['general.QuestionAnswer']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_use': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'general.softwareversion': {
            'Meta': {'ordering': "('-state', '-major', '-minor', '-detail')", 'object_name': 'SoftwareVersion'},
            'changelog': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'detail': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'minor': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'v'", 'max_length': '1'})
        },
        'general.userprofile': {
            'Meta': {'ordering': "['forum_nickname']", 'object_name': 'UserProfile'},
            'categories_voted': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['awards.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'exclude_from_nomination': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'forum_nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_vote': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2010, 1, 1, 0, 0)'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'preference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'refuse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secret_santa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['general']