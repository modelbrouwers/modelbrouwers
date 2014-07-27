from django.db.models.fields import PositiveIntegerField
from .forms import ForumIDField, TopicIDField


class ForumToolsIDField(PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        type_ = kwargs.pop('type')
        assert type_ in ['forum', 'topic']
        self._type = type_
        super(ForumToolsIDField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if self._type == 'forum':
            form_class = ForumIDField
        elif self._type == 'topic':
            form_class = TopicIDField
        defaults = {'form_class': form_class}
        defaults.update(kwargs)
        return super(ForumToolsIDField, self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
rules = [(
        [ForumToolsIDField],
        [],
        {
            'type': ['_type', {'default': None}]
        }
    )
]
add_introspection_rules(rules, ["^forum_tools\.fields\.ForumToolsIDField"])
