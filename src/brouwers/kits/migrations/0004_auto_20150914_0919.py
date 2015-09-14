# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0003_auto_20150722_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scale',
            name='scale',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='scale', db_index=True),
        ),
    ]
