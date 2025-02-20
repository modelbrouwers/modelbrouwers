# Generated by Django 4.2.16 on 2025-02-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_merge_0007_auto_20200426_1617_0007_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="ip_address_joined",
            field=models.GenericIPAddressField(
                blank=True,
                help_text="IP address used during registration.",
                null=True,
                verbose_name="ip address",
            ),
        ),
    ]
