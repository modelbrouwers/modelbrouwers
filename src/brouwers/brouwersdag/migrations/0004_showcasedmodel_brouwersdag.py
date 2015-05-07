# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brouwersdag', '0003_auto_20150405_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='showcasedmodel',
            name='brouwersdag',
            field=models.ForeignKey(to='brouwersdag.Brouwersdag', null=True),
            preserve_default=True,
        ),
    ]
