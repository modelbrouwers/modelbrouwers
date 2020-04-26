# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-29 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cart',
            field=models.ForeignKey(blank=True, help_text='The shopping cart that generated this payment.', null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.Cart', verbose_name='shopping cart'),
        ),
    ]