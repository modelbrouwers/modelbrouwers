# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albums', '0002_auto_20150405_2118'),
        ('migration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumusermigration',
            name='django_user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albummigration',
            name='new_album',
            field=models.ForeignKey(blank=True, to='albums.Album', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='albummigration',
            name='owner',
            field=models.ForeignKey(to='migration.AlbumUserMigration'),
            preserve_default=True,
        ),
    ]
