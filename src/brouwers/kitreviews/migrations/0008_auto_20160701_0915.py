# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 07:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0007_kitreviewproperty_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitreview',
            old_name='topic_id',
            new_name='topic',
        ),
        migrations.AlterField(
            model_name='kitreviewpropertyrating',
            name='kit_review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='kitreviews.KitReview'),
        ),
    ]