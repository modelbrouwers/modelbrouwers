# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-29 13:56
from __future__ import unicode_literals

import brouwers.shop.models.utils
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20190524_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(default=brouwers.shop.models.utils.get_payment_reference, help_text='A unique payment reference', max_length=16, unique=True, verbose_name='reference')),
                ('amount', models.IntegerField(help_text='Amount to be paid, in eurocents.', verbose_name='amount')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='The exact payment data is provider-specific', verbose_name='payment data')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('cart', models.ForeignKey(help_text='The shopping cart that generated this payment.', on_delete=django.db.models.deletion.PROTECT, to='shop.Cart', verbose_name='shopping cart')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.PaymentMethod', verbose_name='Payment method used')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
    ]