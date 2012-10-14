from django import forms
from models import PhotoMigration

class PhotoMigrationForm(forms.Form):
    start = forms.IntegerField(min_value=0, initial=0)
    cnt = PhotoMigration.objects.filter(album__migrated=True, migrated=False).count()
    end = forms.IntegerField(min_value=0, max_value=cnt, initial=2000)