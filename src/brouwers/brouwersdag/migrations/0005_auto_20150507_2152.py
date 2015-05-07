# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_brouwersdag(apps, schema_editor):
    Brouwersdag = apps.get_model('brouwersdag', 'Brouwersdag')
    ShowCasedModel = apps.get_model('brouwersdag', 'ShowCasedModel')

    for model in ShowCasedModel.objects.filter(brouwersdag__isnull=True):
        bd = Brouwersdag.objects.filter(date__gte=model.created).order_by('date').first()
        model.brouwersdag_id = bd.id
        model.save()


class Migration(migrations.Migration):

    dependencies = [
        ('brouwersdag', '0004_showcasedmodel_brouwersdag'),
    ]

    operations = [
        migrations.RunPython(set_brouwersdag),
    ]
