# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-02 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0011_homepagecategory_homepagecategorychild"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="shop/product/", verbose_name="image"
            ),
        ),
    ]
