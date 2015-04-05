# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumMigration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024, blank=True)),
                ('migrated', models.NullBooleanField()),
            ],
            options={
                'ordering': ('owner', 'title'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlbumUserMigration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'album user migration',
                'verbose_name_plural': 'album user migrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoMigration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.CharField(max_length=80)),
                ('filename', models.CharField(max_length=256)),
                ('pwidth', models.PositiveIntegerField(null=True, blank=True)),
                ('pheight', models.PositiveIntegerField(null=True, blank=True)),
                ('title', models.CharField(max_length=512, blank=True)),
                ('caption', models.CharField(max_length=1024, blank=True)),
                ('migrated', models.NullBooleanField()),
                ('album', models.ForeignKey(to='migration.AlbumMigration')),
                ('owner', models.ForeignKey(to='migration.AlbumUserMigration')),
            ],
            options={
                'ordering': ('album',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserMigration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50)),
                ('username_clean', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('hash', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'ordering': ['username_clean'],
            },
            bases=(models.Model,),
        ),
    ]
