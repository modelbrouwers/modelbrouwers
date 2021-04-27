# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-30 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_auto_20180422_1848"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.AddField(
            model_name="product",
            name="categories",
            field=models.ManyToManyField(related_name="products", to="shop.Category"),
        ),
        migrations.AddField(
            model_name="product",
            name="weight_unit",
            field=models.CharField(
                choices=[("g", "Gram"), ("kg", "Kilogram")],
                default="g",
                max_length=10,
                verbose_name="weight unit",
            ),
            preserve_default=False,
        ),
    ]
