# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0009_auto_20150522_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumgroup',
            name='album',
            field=models.OneToOneField(verbose_name='album', to='albums.Album', help_text='Album for which the group has write permissions.'),
        ),
        migrations.AlterField(
            model_name='albumgroup',
            name='users',
            field=models.ManyToManyField(help_text='Users who can write in this album.', to=settings.AUTH_USER_MODEL, verbose_name='users', blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
