# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('language', models.CharField(max_length=10, verbose_name='language', choices=[(b'en', b'English'), (b'nl', b'Dutch')])),
                ('from_date', models.DateTimeField(null=True, blank=True)),
                ('to_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-from_date'],
                'verbose_name': 'announcement',
                'verbose_name_plural': 'announcements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('h', models.CharField(max_length=256, verbose_name='hash')),
                ('expire', models.DateTimeField(verbose_name='expire datetime')),
            ],
            options={
                'ordering': ('expire',),
                'verbose_name': 'password reset',
                'verbose_name_plural': 'password resets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_from', models.CharField(help_text="path from where to redirect, without leading slash.                         E.g. '/shop/' becomse 'shop/'.", unique=True, max_length=255, verbose_name='path from')),
                ('path_to', models.CharField(help_text='Path (relative or absolute to the docroot) or url.', max_length=1024, verbose_name='redirect to')),
            ],
            options={
                'ordering': ('path_from',),
                'verbose_name': 'redirect',
                'verbose_name_plural': 'redirects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegistrationAttempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(default=b'_not_filled_in_', max_length=512, verbose_name='username', db_index=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email', blank=True)),
                ('answer', models.CharField(max_length=255, verbose_name='answer', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('ip_address', models.IPAddressField(verbose_name='IP address', db_index=True)),
                ('success', models.BooleanField(default=False, verbose_name='success')),
                ('type_of_visitor', models.CharField(default=b'normal user', max_length=255, verbose_name='type of visitor')),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'registration attempt',
                'verbose_name_plural': 'registration attempts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegistrationQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(help_text='Question which must be answered for registration.', max_length=255, verbose_name='Anti-spambot question')),
                ('in_use', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SoftwareVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'v', max_length=1, choices=[(b'a', b'alpha'), (b'b', b'beta'), (b'v', b'vanilla')])),
                ('major', models.PositiveSmallIntegerField(default=1)),
                ('minor', models.PositiveSmallIntegerField(default=0)),
                ('detail', models.PositiveSmallIntegerField(default=0, null=True, blank=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('changelog', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-state', '-major', '-minor', '-detail'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_vote', models.DateField(default=datetime.date(2010, 1, 1))),
                ('forum_nickname', models.CharField(unique=True, max_length=30)),
                ('exclude_from_nomination', models.BooleanField(default=False, help_text='If checked, you will be excluded from Awards-nominations.', verbose_name='exclude me from nominations')),
                ('secret_santa', models.BooleanField(default=False, help_text='Aanvinken als je meedoet')),
                ('street', models.CharField(max_length=255, null=True, verbose_name='street name', blank=True)),
                ('number', models.CharField(help_text='house number (+ PO box if applicable)', max_length=10, null=True, verbose_name='number', blank=True)),
                ('postal', models.CharField(max_length=10, null=True, verbose_name='postal code', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name='city', blank=True)),
                ('province', models.CharField(max_length=255, null=True, verbose_name='province', blank=True)),
                ('country', models.CharField(blank=True, max_length=1, null=True, verbose_name='country', choices=[(b'N', 'The Netherlands'), (b'B', 'Belgium'), (b'D', 'Germany'), (b'F', 'France')])),
                ('preference', models.TextField(help_text='Dit wil ik graag', null=True, blank=True)),
                ('refuse', models.TextField(help_text='Dit wil ik absoluut niet', null=True, blank=True)),
                ('allow_sharing', models.BooleanField(default=True, help_text="Checking this gives us permission to share your topics and albums on social media. Uncheck if you don't want to share.", verbose_name='allow social sharing')),
                ('categories_voted', models.ManyToManyField(to='awards.Category', null=True, blank=True)),
            ],
            options={
                'ordering': ['forum_nickname'],
                'verbose_name': 'userprofile',
                'verbose_name_plural': 'userprofiles',
            },
            bases=(models.Model,),
        ),
    ]
