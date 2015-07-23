# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import brouwers.forum_tools.fields
import autoslug.fields
import brouwers.builds.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0003_auto_20150722_2050'),
        ('builds', '0004_auto_20150722_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'ordering': ['scale', 'brand__name'], 'verbose_name': 'build report', 'verbose_name_plural': 'build reports'},
        ),
        migrations.RemoveField(
            model_name='build',
            name='profile',
        ),
        migrations.AddField(
            model_name='build',
            name='forum_topic',
            field=brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', unique=True, null=True, verbose_name='build report topic', blank=True),
        ),
        migrations.AddField(
            model_name='build',
            name='kit',
            field=models.ForeignKey(verbose_name='kit', to='kits.ModelKit', null=True),
        ),
        migrations.AlterField(
            model_name='build',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=brouwers.builds.models.get_build_slug, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='build',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
