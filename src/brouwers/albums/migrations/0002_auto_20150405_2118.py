# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(to='albums.Album'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albumgroup',
            name='album',
            field=models.ForeignKey(verbose_name='album', to='albums.Album', help_text='Album for which the group has write permissions.', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albumgroup',
            name='users',
            field=models.ManyToManyField(help_text='Users who can write in this album.', to=settings.AUTH_USER_MODEL, null=True, verbose_name='users', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albumdownload',
            name='album',
            field=models.ForeignKey(to='albums.Album'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albumdownload',
            name='downloader',
            field=models.ForeignKey(help_text='user who downloaded the album', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='category',
            field=models.ForeignKey(default=1, blank=True, to='albums.Category', null=True, verbose_name='category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover', blank=True, to='albums.Photo', help_text='Image to use as album cover.', null=True, verbose_name='cover'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('user', 'title')]),
        ),
    ]
