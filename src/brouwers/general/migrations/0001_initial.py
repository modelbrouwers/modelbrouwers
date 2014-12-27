# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'general_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], unique=True)),
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
            ('allow_sharing', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'general', ['UserProfile'])

        # Adding M2M table for field categories_voted on 'UserProfile'
        m2m_table_name = db.shorten_name(u'general_userprofile_categories_voted')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'general.userprofile'], null=False)),
            ('category', models.ForeignKey(orm[u'awards.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'category_id'])

        # Adding model 'QuestionAnswer'
        db.create_table(u'general_questionanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'general', ['QuestionAnswer'])

        # Adding model 'RegistrationQuestion'
        db.create_table(u'general_registrationquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('in_use', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'general', ['RegistrationQuestion'])

        # Adding M2M table for field answers on 'RegistrationQuestion'
        m2m_table_name = db.shorten_name(u'general_registrationquestion_answers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('registrationquestion', models.ForeignKey(orm[u'general.registrationquestion'], null=False)),
            ('questionanswer', models.ForeignKey(orm[u'general.questionanswer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['registrationquestion_id', 'questionanswer_id'])

        # Adding model 'RegistrationAttempt'
        db.create_table(u'general_registrationattempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='_not_filled_in_', max_length=512, db_index=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['general.RegistrationQuestion'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, db_index=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_of_visitor', self.gf('django.db.models.fields.CharField')(default='normal user', max_length=255)),
            ('ban', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['banning.Ban'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'general', ['RegistrationAttempt'])

        # Adding model 'SoftwareVersion'
        db.create_table(u'general_softwareversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='v', max_length=1)),
            ('major', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('minor', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('detail', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('changelog', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'general', ['SoftwareVersion'])

        # Adding model 'PasswordReset'
        db.create_table(u'general_passwordreset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('h', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('expire', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'general', ['PasswordReset'])

        # Adding unique constraint on 'PasswordReset', fields ['user', 'h']
        db.create_unique(u'general_passwordreset', ['user_id', 'h'])

        # Adding model 'Redirect'
        db.create_table(u'general_redirect', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path_from', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('path_to', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'general', ['Redirect'])

        # Adding model 'Announcement'
        db.create_table(u'general_announcement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('to_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'general', ['Announcement'])


    def backwards(self, orm):
        # Removing unique constraint on 'PasswordReset', fields ['user', 'h']
        db.delete_unique(u'general_passwordreset', ['user_id', 'h'])

        # Deleting model 'UserProfile'
        db.delete_table(u'general_userprofile')

        # Removing M2M table for field categories_voted on 'UserProfile'
        db.delete_table(db.shorten_name(u'general_userprofile_categories_voted'))

        # Deleting model 'QuestionAnswer'
        db.delete_table(u'general_questionanswer')

        # Deleting model 'RegistrationQuestion'
        db.delete_table(u'general_registrationquestion')

        # Removing M2M table for field answers on 'RegistrationQuestion'
        db.delete_table(db.shorten_name(u'general_registrationquestion_answers'))

        # Deleting model 'RegistrationAttempt'
        db.delete_table(u'general_registrationattempt')

        # Deleting model 'SoftwareVersion'
        db.delete_table(u'general_softwareversion')

        # Deleting model 'PasswordReset'
        db.delete_table(u'general_passwordreset')

        # Deleting model 'Redirect'
        db.delete_table(u'general_redirect')

        # Deleting model 'Announcement'
        db.delete_table(u'general_announcement')


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
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ban': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['banning.Ban']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['general.RegistrationQuestion']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type_of_visitor': ('django.db.models.fields.CharField', [], {'default': "'normal user'", 'max_length': '255'}),
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

    complete_apps = ['general']