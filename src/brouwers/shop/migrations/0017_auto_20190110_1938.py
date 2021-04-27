# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-10 18:38
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0016_auto_20181217_2121"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[("open", "Open"), ("paid", "Paid")],
                default="open",
                max_length=10,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="cartproduct",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="shop.Cart",
            ),
        ),
    ]
