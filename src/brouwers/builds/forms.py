import re

from django import forms

from brouwers.kits.models import Brand, Scale
from .models import Build


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ('title', 'kits', 'topic', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'date'}),
        }
        localized_fields = '__all__'


class BuildFormForum(forms.ModelForm):

    """
    Form to enable quick instantiating of a Build object trough GET QueryDict
    """

    class Meta:
        model = Build
        fields = ('topic', 'title')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BuildFormForum, self).__init__(*args, **kwargs)

    def get_build(self):
        """
        Pre-fill some build attributes based on GET parameters
        """
        build = Build(
            topic_id=self.cleaned_data['topic_id'],
            user_id=self.request.user.id,
            title=self.cleaned_data['title'],
        )

        # Try to parse the scale
        pattern = re.compile(r'1[:/](\d{1,4})')
        match = re.search(pattern, build.title)
        if match:
            build.scale, created = Scale.objects.get_or_create(scale=match.group(1))

        # see if we can match a brand...
        bits = build.title.split()
        for bit in bits:
            build.brand = Brand.objects.filter(name__iexact=bit).first()

        return build
