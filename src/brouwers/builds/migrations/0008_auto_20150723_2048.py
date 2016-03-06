# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0007_auto_20150723_2023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'ordering': ['kits__scale', 'brand__name'], 'verbose_name': 'build report', 'verbose_name_plural': 'build reports'},
        ),
        migrations.RemoveField(
            model_name='build',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='build',
            name='forum_id',
        ),
        migrations.RemoveField(
            model_name='build',
            name='scale',
        ),
        migrations.RemoveField(
            model_name='build',
            name='topic_id',
        ),
        migrations.RemoveField(
            model_name='build',
            name='url',
        ),
    ]
