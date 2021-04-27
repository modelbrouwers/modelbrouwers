# Generated by Django 2.0.13 on 2020-04-26 14:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_user_customer_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="customer_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="users",
                to="shop.CustomerGroup",
            ),
        ),
    ]
