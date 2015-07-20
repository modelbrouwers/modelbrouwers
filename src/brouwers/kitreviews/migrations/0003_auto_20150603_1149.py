# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0002_auto_20150405_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelkit',
            name='duplicates',
            field=models.ManyToManyField(help_text='Kits that are the same but have another producer.', related_name='duplicates_rel_+', verbose_name='duplicates', to='kitreviews.ModelKit', blank=True),
        ),
    ]
