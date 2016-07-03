from django.forms import ModelForm


class AlwaysChangedModelForm(ModelForm):
    """
    Mark the form always as changed, so that the instance is always saved.
    """

    def has_changed(self):
        return True
