# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0003_auto_20150603_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelkit',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='modelkit',
            name='category',
        ),
        migrations.RemoveField(
            model_name='modelkit',
            name='duplicates',
        ),
        migrations.RemoveField(
            model_name='modelkit',
            name='scale',
        ),
        migrations.RemoveField(
            model_name='modelkit',
            name='submitter',
        ),
        migrations.AlterField(
            model_name='kitreview',
            name='model_kit',
            field=models.ForeignKey(to='kits.ModelKit'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='ModelKit',
        ),
        migrations.DeleteModel(
            name='Scale',
        ),
    ]
