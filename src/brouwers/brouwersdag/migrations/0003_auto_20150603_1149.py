# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brouwersdag', '0002_auto_20150507_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showcasedmodel',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='e-mail address'),
        ),
    ]
