# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('banning', '0002_ban_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registrationquestion',
            name='answers',
            field=models.ManyToManyField(to='general.QuestionAnswer', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registrationattempt',
            name='ban',
            field=models.OneToOneField(null=True, blank=True, to='banning.Ban'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='registrationattempt',
            name='question',
            field=models.ForeignKey(verbose_name='registration question', to='general.RegistrationQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='passwordreset',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='passwordreset',
            unique_together=set([('h', 'user')]),
        ),
    ]
