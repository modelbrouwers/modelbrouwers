from ..models import Preferences


class override_preferences(object):

    def __init__(self, user, **kwargs):
        assert len(kwargs), 'You must provide at least one field'
        self.kwargs = kwargs
        # make sure the prefs object is created for the user
        prefs_obj, created = Preferences.objects.get_or_create(user=user)
        self.pref_obj = prefs_obj
        self.old_values = {}

    def __enter__(self, ):
        for field, value in self.kwargs.items():
            self.old_values[field] = getattr(self.pref_obj, field)
            setattr(self.pref_obj, field, value)

        self.pref_obj.save()

    def __exit__(self, exc_type, exc_value, traceback):
        for field, value in self.old_values.items():
            setattr(self.pref_obj, field, value)
        self.pref_obj.save()
