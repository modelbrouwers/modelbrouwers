# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0007_auto_20150520_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=b'256', verbose_name='album title', db_index=True),
            preserve_default=True,
        ),
    ]
