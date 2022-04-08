from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("awards", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="user",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="project",
            name="category",
            field=models.ForeignKey(
                verbose_name="categorie", to="awards.Category", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="project",
            name="last_reviewer",
            field=models.ForeignKey(
                verbose_name="last reviewer",
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="project",
            name="submitter",
            field=models.ForeignKey(
                related_name="nominations",
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="project",
            unique_together=set([("category", "url")]),
        ),
    ]
