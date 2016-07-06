# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0008_auto_20160701_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('categorie_id', models.AutoField(primary_key=True, serialize=False)),
                ('naam', models.TextField()),
            ],
            options={
                'db_table': 'categorieen',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Fabrikant',
            fields=[
                ('fabrikant_id', models.AutoField(primary_key=True, serialize=False)),
                ('naam', models.TextField()),
            ],
            options={
                'db_table': 'fabrikanten',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('kit_id', models.AutoField(primary_key=True, serialize=False)),
                ('modelnaam', models.TextField()),
                ('type', models.TextField()),
                ('schaal', models.SmallIntegerField()),
                ('moeilijkheid', models.IntegerField()),
                ('categorie', models.ForeignKey(to='kitreviews.Categorie')),
                ('foto', models.TextField(blank=True, null=True)),
                ('fabrikant', models.ForeignKey(to='kitreviews.Fabrikant')),
                ('te_koop', models.CharField(max_length=3)),
                ('url_shop', models.TextField(blank=True, null=True)),
                ('datum', models.DateTimeField()),
                ('bouwbeschrijving', models.TextField()),
            ],
            options={
                'db_table': 'kits',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('commentaar', models.TextField()),
                ('url_bouwverslag_mb', models.TextField(blank=True, null=True)),
                ('url_album', models.TextField(blank=True, null=True)),
                ('url_bouwverslag_twenot', models.TextField(blank=True, null=True)),
                ('pluspunten', models.TextField(blank=True, null=True)),
                ('minpunten', models.TextField(blank=True, null=True)),
                ('indruk', models.IntegerField()),
                ('kit', models.ForeignKey(to='kitreviews.Kit')),
                ('reviewer', models.ForeignKey(to='kitreviews.Reviewer')),
                ('datum', models.DateTimeField()),
            ],
            options={
                'db_table': 'reviews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('reviewer_id', models.AutoField(primary_key=True, serialize=False)),
                ('naam', models.TextField()),
                ('emailadres', models.TextField()),
            ],
            options={
                'db_table': 'reviewers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Uitbreiding',
            fields=[
                ('uitbreiding_id', models.AutoField(primary_key=True, serialize=False)),
                ('naam', models.TextField()),
                ('fabrikantnaam', models.TextField()),
                ('kit', models.ForeignKey(to='kitreviews.Kit'))
            ],
            options={
                'db_table': 'uitbreidingen',
                'managed': False,
            },
        ),
    ]
