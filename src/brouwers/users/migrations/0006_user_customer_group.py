# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-18 16:30
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0016_auto_20181217_2121"),
        ("users", "0005_datadownloadrequest_downloaded"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="customer_group",
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="shop.CustomerGroup",
            ),
        ),
    ]
