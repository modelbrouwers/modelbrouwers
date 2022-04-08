# Generated by Django 1.10 on 2016-08-11 20:30


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("kits", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Brouwersdag",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("date", models.DateField(blank=True, verbose_name="date")),
            ],
            options={
                "ordering": ("-date",),
                "verbose_name": "brouwersdag",
                "verbose_name_plural": "brouwersdagen",
            },
        ),
        migrations.CreateModel(
            name="Competition",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default="0.0",
                        max_digits=5,
                        verbose_name="price per model",
                    ),
                ),
                (
                    "max_num_models",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Maximum number of models per participant, enter 0 for unlimited.",
                        verbose_name="models per participant",
                    ),
                ),
                (
                    "max_participants",
                    models.PositiveSmallIntegerField(
                        default=0,
                        help_text="Maximum number of participants, enter 0 for unlimited.",
                        verbose_name="maximum number of participants",
                    ),
                ),
                (
                    "is_current",
                    models.BooleanField(
                        default=False,
                        help_text="Marking this competition as active will deactivate all other competitions.",
                        verbose_name="current open competition?",
                    ),
                ),
            ],
            options={
                "verbose_name": "competition",
                "verbose_name_plural": "competitions",
            },
        ),
        migrations.CreateModel(
            name="Exhibitor",
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
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("website", models.URLField(blank=True, verbose_name="website")),
                (
                    "space",
                    models.CharField(
                        blank=True,
                        help_text="Amount of space needed. 100 characters or less.",
                        max_length=100,
                        verbose_name="space needed",
                    ),
                ),
                (
                    "brouwersdag",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="brouwersdag.Brouwersdag",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "exhibitor",
                "verbose_name_plural": "exhibitors",
            },
        ),
        migrations.CreateModel(
            name="ShowCasedModel",
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
                    "owner_name",
                    models.CharField(max_length=254, verbose_name="real name"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="e-mail address"),
                ),
                ("name", models.CharField(max_length=254, verbose_name="model name")),
                (
                    "scale",
                    models.PositiveSmallIntegerField(
                        help_text='Enter the number after the "1:" or "1/". E.g. 1/48 --> enter 48.',
                        verbose_name="scale",
                    ),
                ),
                (
                    "remarks",
                    models.TextField(
                        blank=True,
                        help_text='Add the features that make this model special here, e.g. "scratch built cockpit"',
                        verbose_name="remarkable elements",
                    ),
                ),
                ("topic", models.URLField(blank=True, verbose_name="topic url")),
                (
                    "length",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="In cm.", null=True, verbose_name="length"
                    ),
                ),
                (
                    "width",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="In cm.", null=True, verbose_name="width"
                    ),
                ),
                (
                    "height",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="In cm.", null=True, verbose_name="height"
                    ),
                ),
                (
                    "is_competitor",
                    models.BooleanField(
                        default=False, verbose_name="enter competition?"
                    ),
                ),
                (
                    "is_paid",
                    models.BooleanField(
                        default=False, verbose_name="competition fee paid?"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="added"),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="kits.Brand",
                        verbose_name="brand",
                    ),
                ),
                (
                    "brouwersdag",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="brouwersdag.Brouwersdag",
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="brouwersdag.Competition",
                        verbose_name="competition",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="brouwer",
                    ),
                ),
            ],
            options={
                "verbose_name": "showcased model",
                "verbose_name_plural": "showcased models",
            },
        ),
    ]
