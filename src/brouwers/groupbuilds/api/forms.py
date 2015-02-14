from django import forms

from brouwers.forum_tools.forms.fields import ForumIDField, TopicIDField


class TopicDetailsForm(forms.Form):
    forum_id = ForumIDField()
    topic_id = TopicIDField(required=False)
