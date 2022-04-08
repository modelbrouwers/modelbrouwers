import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField()),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "url",
                    models.URLField(help_text="link naar het verslag", max_length=500),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="titel verslag"),
                ),
                ("brouwer", models.CharField(max_length=30)),
                (
                    "image",
                    models.ImageField(null=True, upload_to="awards/", blank=True),
                ),
                (
                    "nomination_date",
                    models.DateField(default=datetime.date.today, db_index=True),
                ),
                ("votes", models.IntegerField(default=0, null=True, blank=True)),
                ("rejected", models.BooleanField(default=False)),
                (
                    "last_review",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last review", null=True
                    ),
                ),
            ],
            options={
                "ordering": ["category", "votes"],
                "verbose_name": "nomination",
                "verbose_name_plural": "nominations",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("submitted", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(to="awards.Category", on_delete=models.CASCADE),
                ),
                (
                    "project1",
                    models.ForeignKey(
                        related_name="+", to="awards.Project", on_delete=models.CASCADE
                    ),
                ),
                (
                    "project2",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="awards.Project",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "project3",
                    models.ForeignKey(
                        related_name="+",
                        blank=True,
                        to="awards.Project",
                        null=True,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
