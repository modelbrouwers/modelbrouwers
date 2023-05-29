# Generated by Django 3.2.16 on 2022-12-31 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0038_auto_20221229_1747"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="payment",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="cart",
        ),
        migrations.AddField(
            model_name="order",
            name="reference",
            field=models.CharField(
                default="",
                help_text="A unique order reference",
                max_length=16,
                unique=True,
                verbose_name="reference",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="historical_order",
            field=models.ForeignKey(
                blank=True,
                help_text="Order this payment was for, in case it was cancelled/aborted. You cannot set order and historical order at the same time.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="historical_payments",
                to="shop.order",
                verbose_name="historical order",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="order",
            field=models.OneToOneField(
                default=1,
                help_text="The order being paid by this payment.",
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.order",
                verbose_name="order",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="status",
            field=models.CharField(
                choices=[
                    ("open", "Open"),
                    ("processing", "Processing"),
                    ("closed", "Closed"),
                ],
                default="open",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="cart",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                to="shop.cart",
                verbose_name="shopping cart",
            ),
        ),
        migrations.AddConstraint(
            model_name="payment",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("historical_order__isnull", False),
                    ("order__isnull", False),
                    _negated=True,
                ),
                name="order_or_historical_order",
            ),
        ),
    ]