# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('brouwersdag', '0001_squashed_0006_auto_20150507_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brouwersdag',
            name='date',
            field=models.DateField(default=datetime.date(2014, 9, 27), verbose_name='date', blank=True),
            preserve_default=False,
        ),
    ]
