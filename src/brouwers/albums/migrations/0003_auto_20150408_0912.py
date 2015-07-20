# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import brouwers.forum_tools.fields
import brouwers.albums.models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20150405_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='topic',
            field=brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='build report topic', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(default=b'', max_length=b'256', verbose_name='album title', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='album',
            name='writable_to',
            field=models.CharField(default=b'u', help_text='Specify who can upload images in this album', max_length=1, verbose_name='writable to', choices=[(b'u', 'owner'), (b'g', 'group'), (b'o', 'everyone')]),
            preserve_default=True,
        ),
    ]
