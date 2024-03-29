# Generated by Django 3.2.18 on 2023-04-10 14:45

from django.db import migrations, models

import brouwers.builds.validators


class Migration(migrations.Migration):

    dependencies = [
        ("builds", "0002_buildphoto_image_gone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buildphoto",
            name="photo_url",
            field=models.URLField(
                blank=True,
                help_text="Link to an image",
                validators=[brouwers.builds.validators.ImageURLValidator()],
            ),
        ),
    ]
