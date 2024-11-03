# Generated by Django 4.2.16 on 2024-09-26 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("anniversaries", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="remarkableevent",
            name="image_alt_text",
            field=models.TextField(
                blank=True,
                help_text="Describe what's visible in the image for users with visual impairments. An alt text is required if you upload an image.",
                verbose_name="image alt text",
            ),
        ),
    ]