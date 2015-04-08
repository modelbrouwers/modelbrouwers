# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='brand', db_index=True)),
                ('logo', models.ImageField(upload_to=b'images/brand_logos/', null=True, verbose_name='logo', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Does the brand still exist?', db_index=True, verbose_name='is active?')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'brand',
                'verbose_name_plural': 'brands',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KitReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('raw_text', models.TextField(help_text='This is your review. You can use BBCode here.', verbose_name='review')),
                ('html', models.TextField(help_text='raw_text with BBCode rendered as html', blank=True)),
                ('positive_points', models.TextField(verbose_name='positive points', blank=True)),
                ('negative_points', models.TextField(verbose_name='negative points', blank=True)),
                ('rating', models.PositiveSmallIntegerField(default=50, verbose_name='rating')),
                ('topic_id', models.PositiveIntegerField(help_text='ID of the topic on Modelbrouwers.', null=True, verbose_name='topic', blank=True)),
                ('external_topic_url', models.URLField(help_text='URL to the topic not hosted on Modelbrouwers', verbose_name='topic url', blank=True)),
                ('show_real_name', models.BooleanField(default=True, help_text='Checking this option will display your real name as reviewer. Uncheck to use your nickname.', verbose_name='show real name?')),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'kit review',
                'verbose_name_plural': 'kit reviews',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KitReviewVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.CharField(max_length=1, verbose_name='vote', db_index=True)),
            ],
            options={
                'verbose_name': 'kit review vote',
                'verbose_name_plural': 'kit review votes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModelKit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kit_number', models.CharField(help_text='Kit number as found on the box.', max_length=50, verbose_name='kit number', db_index=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='kit name', db_index=True)),
                ('difficulty', models.PositiveSmallIntegerField(default=3, verbose_name='difficulty')),
                ('box_image', models.ImageField(upload_to=b'kits/box_images/%Y/%m', null=True, verbose_name='box image', blank=True)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(verbose_name='brand', to='kitreviews.Brand')),
                ('category', models.ForeignKey(verbose_name='category', to='kitreviews.Category', null=True)),
                ('duplicates', models.ManyToManyField(related_name='duplicates_rel_+', to='kitreviews.ModelKit', blank=True, help_text='Kits that are the same but have another producer.', null=True, verbose_name='duplicates')),
            ],
            options={
                'verbose_name': 'model kit',
                'verbose_name_plural': 'model kits',
            },
            bases=(models.Model,),
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
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='modelkit',
            name='scale',
            field=models.ForeignKey(verbose_name='scale', to='kitreviews.Scale'),
            preserve_default=True,
        ),
    ]
