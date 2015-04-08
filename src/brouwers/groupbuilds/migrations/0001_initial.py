# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import brouwers.forum_tools.fields
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupBuild',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forum', brouwers.forum_tools.fields.ForumToolsIDField(help_text='Forum id of the group build subforum', type=b'forum', null=True, verbose_name='forum id', blank=True)),
                ('theme', models.CharField(help_text='Theme/name of the group build', max_length=100, verbose_name='theme')),
                ('slug', autoslug.fields.AutoSlugField(unique=True, verbose_name='slug')),
                ('description', models.TextField(help_text='Short description', verbose_name='description')),
                ('start', models.DateField(help_text='Date when you want to start building.', null=True, verbose_name='start date', blank=True)),
                ('end', models.DateField(help_text='Date this build ends.', null=True, verbose_name='end date', blank=True)),
                ('duration', models.PositiveSmallIntegerField(default=92, verbose_name='duration', choices=[(30, '30 days'), (61, '2 months'), (92, '3 months'), (183, '6 months'), (365, 'one year')])),
                ('status', models.CharField(default=b'concept', max_length=10, verbose_name='status', choices=[(b'concept', 'concept/idea'), (b'submitted', 'submitted for review'), (b'accepted', 'accepted'), (b'denied', 'denied'), (b'extended', 'extended')])),
                ('users_can_vote', models.BooleanField(default=False, help_text='Let users vote to determine the build popularity', verbose_name='users can vote')),
                ('upvotes', models.PositiveSmallIntegerField(null=True, verbose_name='upvotes', blank=True)),
                ('downvotes', models.PositiveSmallIntegerField(null=True, verbose_name='downvotes', blank=True)),
                ('rules', models.TextField(blank=True)),
                ('rules_topic', brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='rules topic', blank=True)),
                ('homepage_topic', brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='topic to direct to from calendar', blank=True)),
                ('introduction_topic', brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='introduction topic', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('reason_denied', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'verbose_name': 'group build',
                'verbose_name_plural': 'group builds',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=255, verbose_name='model name', blank=True)),
                ('finished', models.BooleanField(default=False, verbose_name='finished')),
                ('topic', brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='topic', blank=True)),
                ('points', models.SmallIntegerField(null=True, verbose_name='points', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('groupbuild', models.ForeignKey(to='groupbuilds.GroupBuild')),
            ],
            options={
                'verbose_name': 'group build participant',
                'verbose_name_plural': 'group build participants',
            },
            bases=(models.Model,),
        ),
    ]
