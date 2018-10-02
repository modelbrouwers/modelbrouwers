# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-22 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20180422_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_de',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_nl',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_de',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_nl',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
    ]