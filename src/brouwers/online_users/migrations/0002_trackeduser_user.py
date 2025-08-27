from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("online_users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trackeduser",
            name="user",
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
    ]
