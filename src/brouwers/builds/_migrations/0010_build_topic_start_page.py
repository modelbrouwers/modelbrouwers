# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0009_auto_20150723_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='topic_start_page',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='topic start page'),
        ),
    ]
