# Models generated via ``src/manage.py inspectdb --database legacy_shop``
from django.db import models


class OcSetting(models.Model):
    setting_id = models.AutoField(primary_key=True)
    store_id = models.IntegerField()
    group = models.CharField(max_length=32)
    key = models.CharField(max_length=64)
    value = models.TextField()
    serialized = models.IntegerField()

    class Meta:
        managed = False
        db_table = "oc_setting"
