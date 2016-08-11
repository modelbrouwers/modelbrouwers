# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('url', models.URLField(help_text='link to the build report', unique=True, max_length=500)),
                ('topic_id', models.PositiveIntegerField(help_text='PHPBB topic id, used to build the link to the topic.', unique=True, null=True, verbose_name='Topic ID', blank=True)),
                ('forum_id', models.PositiveIntegerField(help_text="Used to determine the 'category'.", null=True, verbose_name='Forum ID', blank=True)),
                ('title', models.CharField(help_text='Enter a descriptive build title.', max_length=255, verbose_name='title')),
                ('scale', models.PositiveSmallIntegerField(help_text='Enter the number after the "1:" or "1/". E.g. 1/48 --> enter 48.', null=True, verbose_name='scale', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='end date', blank=True)),
            ],
            options={
                'ordering': ['profile', 'scale', 'brand__name'],
                'verbose_name': 'build report',
                'verbose_name_plural': 'build reports',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo_url', models.URLField(help_text='Link to an image', blank=True)),
                ('order', models.PositiveSmallIntegerField(help_text='Order in which photos are shown', null=True, blank=True)),
                ('build', models.ForeignKey(verbose_name='build', to='builds.Build')),
                ('photo', models.OneToOneField(null=True, blank=True, to='albums.Photo')),
            ],
            options={
                'ordering': ['order', 'id'],
                'verbose_name': 'build photo',
                'verbose_name_plural': 'build photos',
            },
            bases=(models.Model,),
        ),
    ]
