from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("online_users", "0002_trackeduser_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trackeduser",
            name="user",
            field=models.OneToOneField(
                to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
            ),
        ),
    ]
