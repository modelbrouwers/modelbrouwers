# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20150405_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(default=b'album 07-05-2015', max_length=b'256', verbose_name='album title', db_index=True),
            preserve_default=True,
        ),
    ]
