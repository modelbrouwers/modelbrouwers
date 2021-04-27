# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-30 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("nl", "Dutch"), ("de", "German")],
                max_length=10,
                verbose_name="language",
            ),
        ),
        migrations.AlterField(
            model_name="registrationquestion",
            name="lang",
            field=models.CharField(
                choices=[("en", "English"), ("nl", "Dutch"), ("de", "German")],
                default="nl",
                max_length=10,
                verbose_name="language",
            ),
        ),
    ]
