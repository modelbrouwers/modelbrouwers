# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-24 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_paymentmethod_shopconfiguration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentmethod',
            old_name='enabeld',
            new_name='enabled',
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='name_de',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='paymentmethod',
            name='name_nl',
            field=models.CharField(max_length=50, null=True, verbose_name='name'),
        ),
    ]