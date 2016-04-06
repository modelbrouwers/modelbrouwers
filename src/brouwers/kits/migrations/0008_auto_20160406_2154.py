# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0007_auto_20160313_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(db_index=True, error_messages={b'unique': 'This brand already exists'}, max_length=100, unique=True, verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='scale',
            name='scale',
            field=models.PositiveSmallIntegerField(db_index=True, error_messages={b'unique': 'This scale already exists'}, unique=True, verbose_name='scale'),
        ),
    ]
