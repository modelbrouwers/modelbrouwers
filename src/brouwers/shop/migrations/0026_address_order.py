# Generated by Django 3.2.13 on 2022-06-19 12:33

import django.db.models.deletion
from django.db import migrations, models

import brouwers.general.fields


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0025_cart_snapshot_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "street",
                    models.CharField(max_length=255, verbose_name="street name"),
                ),
                (
                    "number",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="house number"
                    ),
                ),
                (
                    "postal_code",
                    models.CharField(max_length=50, verbose_name="postal code"),
                ),
                ("city", models.CharField(max_length=255, verbose_name="city")),
                (
                    "country",
                    brouwers.general.fields.CountryField(
                        choices=[
                            ("N", "The Netherlands"),
                            ("B", "Belgium"),
                            ("D", "Germany"),
                            ("F", "France"),
                        ],
                        max_length=1,
                        verbose_name="country",
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="company"
                    ),
                ),
                (
                    "chamber_of_commerce",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name="chamber of commerce number",
                    ),
                ),
            ],
            options={
                "verbose_name": "address",
                "verbose_name_plural": "addresses",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("received", "Received"),
                            ("processing", "Processing"),
                            ("shipped", "Shipped"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=255, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="last name"
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "phone",
                    models.CharField(max_length=100, verbose_name="phone number"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="shop.cart",
                        verbose_name="shopping cart",
                    ),
                ),
                (
                    "delivery_address",
                    models.OneToOneField(
                        help_text="Address for delivery",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="delivery_order",
                        to="shop.address",
                    ),
                ),
                (
                    "invoice_address",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="invoice_order",
                        to="shop.address",
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="shop.payment",
                        verbose_name="payment instance",
                    ),
                ),
            ],
            options={
                "verbose_name": "order",
                "verbose_name_plural": "orders",
            },
        ),
    ]
