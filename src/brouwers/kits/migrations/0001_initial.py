# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import brouwers.kits.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='brand', db_index=True)),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', unique=True, editable=False)),
                ('logo', models.ImageField(upload_to=b'images/brand_logos/', verbose_name='logo', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Whether the brand still exists or not', db_index=True, verbose_name='is active')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
        ),
        migrations.CreateModel(
            name='ModelKit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='kit name', db_index=True)),
                ('slug', autoslug.fields.AutoSlugField(verbose_name='slug', unique=True, editable=False)),
                ('kit_number', models.CharField(help_text='Kit number as found on the box.', max_length=50, verbose_name='kit number', db_index=True, blank=True)),
                ('difficulty', models.PositiveSmallIntegerField(default=30, choices=[(10, 'very easy'), (20, 'easy'), (30, 'medium'), (40, 'hard'), (50, 'very hard')], verbose_name='difficulty', validators=[brouwers.kits.models.difficulty_valid])),
                ('box_image', models.ImageField(upload_to=b'kits/box_images/%Y/%m', verbose_name='box image', blank=True)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(verbose_name='brand', to='kits.Brand')),
                ('duplicates', models.ManyToManyField(help_text='Kits that are the same but have another producer.', related_name='duplicates_rel_+', verbose_name='duplicates', to='kits.ModelKit', blank=True)),
            ],
            options={
                'verbose_name': 'model kit',
                'verbose_name_plural': 'model kits',
            },
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scale', models.PositiveSmallIntegerField(verbose_name='scale', db_index=True)),
            ],
            options={
                'ordering': ['scale'],
                'verbose_name': 'scale',
                'verbose_name_plural': 'scales',
            },
        ),
        migrations.AddField(
            model_name='modelkit',
            name='scale',
            field=models.ForeignKey(verbose_name='scale', to='kits.Scale'),
        ),
        migrations.AddField(
            model_name='modelkit',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
