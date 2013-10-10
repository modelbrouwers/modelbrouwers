from django import forms
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _


from kitreviews.models import Brand


from models import Build


import re


class SearchForm(forms.Form):
    search_term = forms.CharField(
                    max_length=100, required=False,
                    widget=forms.TextInput(attrs={
                        'placeholder': _('Enter a keyword or the '
                                         'name of the builder'),
                        })
                    )


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        exclude = (
            'profile', 
            'nomination', 
            'user', 
            'slug', 
            'topic_id', 
            'forum_id', 
            'brand_name'
            )
    
    def __init__(self, *args, **kwargs):
        is_edit = kwargs.pop('is_edit', False)
        super(BuildForm, self).__init__(*args, **kwargs)
        if is_edit:
            del self.fields['url']

    def clean_url(self):
        url = self.cleaned_data['url']
        match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
        if not match:
            match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?t=(\d+)&f=(\d+)', url)
            if not match:
                raise forms.ValidationError(_("This URL doesn't point to a forum topic."))
        self.cleaned_data['url'] = "http://www.%s" % match.group(0)
        return self.cleaned_data['url']


class BuildFormForum(forms.ModelForm):
    """ Form to enable quick instantiating of a Build object trough GET QueryDict """
    class Meta:
        model = Build
        fields = ('forum_id', 'topic_id', 'title')


    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BuildFormForum, self).__init__(*args, **kwargs)

    def get_build(self):
        """ Pre-fill some build attributes based on GET parameters """
        build = Build(
            forum_id = self.cleaned_data['forum_id'],
            topic_id = self.cleaned_data['topic_id'],
            user_id = self.request.user.id,
            profile_id = self.request.user.get_profile().id,
            title = self.cleaned_data['title'],
            )
        
        # create url
        current_site = get_current_site(self.request)
        build.url = "http://%s%s" % (current_site.domain, build.topic_url)

        # Try to parse the scale
        pattern = re.compile(r'1[:/](\d{1,4})')
        match = re.search(pattern, build.title)
        if match:
            build.scale = match.group(1)

        # see if we can match a brand...
        bits = build.title.split()
        for bit in bits:
            brands = Brand.objects.filter(name__iexact=bit)
            if brands:
                build.brand = brands[0]

        return build

