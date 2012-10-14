from django import forms
from django.conf import settings
from models import PhotoMigration

class PhotoMigrationForm(forms.Form):
    start = forms.IntegerField(min_value=0, initial=0)
    cnt = PhotoMigration.objects.filter(album__migrated=True, migrated=False).count()
    if settings.DEBUG:
        cnt = 100000
    end = forms.IntegerField(min_value=0, max_value=cnt, initial=2000)
