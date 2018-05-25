# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0002_auto_20160816_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='kitreview',
            name='is_reviewed',
            field=models.BooleanField(default=False, verbose_name='is reviewed?'),
        ),
        migrations.AlterField(
            model_name='kitreview',
            name='external_topic_url',
            field=models.URLField(blank=True, help_text='URL to the topic not hosted on Modelbrouwers', verbose_name='external topic url'),
        ),
    ]