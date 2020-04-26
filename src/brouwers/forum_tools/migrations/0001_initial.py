# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.conf import settings
from django.db import models, migrations
import brouwers.forum_tools.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuildReportsForum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forum', brouwers.forum_tools.fields.ForumToolsIDField(type='forum', verbose_name='forum')),
            ],
            options={
                'ordering': ['forum'],
                'verbose_name': 'build report forum',
                'verbose_name_plural': 'build report forums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('forum_id', models.AutoField(serialize=False, primary_key=True)),
                ('forum_name', models.CharField(max_length=60)),
                ('forum_topics', models.IntegerField(default=0)),
                ('forum_posts', models.IntegerField(default=0)),
                ('forum_desc', models.TextField()),
                ('parent', models.ForeignKey(
                    related_name='child',
                    default=None,
                    to='forum_tools.Forum',
                    null=True,
                    blank=True,
                    on_delete=models.CASCADE,
                )),
            ],
            options={
                'ordering': ['forum_name'],
                'db_table': '%sforums' % settings.PHPBB_TABLE_PREFIX,
                'managed': settings.TESTING,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('forum', brouwers.forum_tools.fields.ForumToolsIDField(type='forum', null=True, verbose_name='forum', blank=True)),
                ('icon_class', models.CharField(max_length=50, verbose_name='icon class', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'forum category',
                'verbose_name_plural': 'forum categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumLinkBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_id', models.CharField(help_text='HTML id of the base anchor.', max_length=128, verbose_name='link id')),
                ('short_description', models.CharField(max_length=64, verbose_name='short description', blank=True)),
                ('enabled', models.BooleanField(default=True, help_text='Enable the syncing of this link.', verbose_name='enabled')),
                ('from_date', models.DateField(help_text='Start date from when this link is enabled.', verbose_name='from date')),
                ('to_date', models.DateField(help_text='End date from when this link is enabled, this date included.', verbose_name='to date')),
            ],
            options={
                'verbose_name': 'base forum link',
                'verbose_name_plural': 'base forum links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumLinkSynced',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_id', models.CharField(help_text='HTML id of the anchor to be synced.', max_length=128, verbose_name='link id')),
                ('base', models.ForeignKey(verbose_name='base link', to='forum_tools.ForumLinkBase', help_text='Link this link syncs with.', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'synced forum link',
                'verbose_name_plural': 'synced forum links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumPostCountRestriction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forum', brouwers.forum_tools.fields.ForumToolsIDField(type='forum', null=True, verbose_name='forum id', blank=True)),
                ('min_posts', models.PositiveSmallIntegerField(verbose_name='minimum number of posts')),
                ('posting_level', models.CharField(max_length=1, verbose_name='posting level', choices=[('T', 'Topic'), ('R', 'Reply')])),
            ],
            options={
                'ordering': ['forum'],
                'verbose_name': 'forum post count restriction',
                'verbose_name_plural': 'forum post count restrictions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('user_id', models.AutoField(help_text='Primary key', serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=255, verbose_name='username')),
                ('username_clean', models.CharField(max_length=255, verbose_name='username')),
                ('user_posts', models.IntegerField()),
                ('user_email', models.CharField(max_length=100, verbose_name='email')),
                ('user_email_hash', models.BigIntegerField(default=0, help_text="A hash of the user's email address.", db_column='user_email_hash')),
                ('user_permissions', models.TextField(blank=True)),
                ('user_sig', models.TextField(blank=True)),
                ('user_interests', models.TextField(blank=True)),
                ('user_actkey', models.TextField(blank=True)),
                ('user_occ', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('username',),
                'db_table': '%susers' % settings.PHPBB_TABLE_PREFIX,
                'verbose_name': 'forum user',
                'verbose_name_plural': 'forum users',
                'managed': settings.TESTING,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(help_text='Primary key', serialize=False, primary_key=True)),
                ('report_closed', models.BooleanField(default=False, help_text='Closed reports need no more attention.', verbose_name='closed')),
                ('report_time_int', models.IntegerField(help_text='UNIX time when the report was added.', verbose_name='time', db_column='report_time')),
                ('report_text', models.TextField(verbose_name='text', blank=True)),
            ],
            options={
                'db_table': '%sreports' % settings.PHPBB_TABLE_PREFIX,
                'verbose_name': 'report',
                'verbose_name_plural': 'reports',
                'permissions': (('can_see_reports', 'Can see (number of) open reports'),),
                'managed': settings.TESTING,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.AutoField(serialize=False, primary_key=True)),
                ('topic_title', models.CharField(max_length=255)),
                ('last_post_time', models.BigIntegerField(default=0, db_column='topic_last_post_time')),
                ('create_time', models.BigIntegerField(default=0, db_column='topic_time')),
                ('forum', models.ForeignKey(to='forum_tools.Forum', on_delete=models.CASCADE)),
                ('author', models.ForeignKey(
                    to='forum_tools.ForumUser', db_column='topic_poster',
                    null=True, blank=True,
                    on_delete=models.SET_NULL,
                )),
            ],
            options={
                'ordering': ['topic_id'],
                'db_table': '%stopics' % settings.PHPBB_TABLE_PREFIX,
                'managed': settings.TESTING,
            },
            bases=(models.Model,),
        ),
    ]
