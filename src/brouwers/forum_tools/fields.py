from django.db.models.fields import PositiveIntegerField


class ForumToolsIDField(PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        type_ = kwargs.pop('type')
        assert type_ in ['forum', 'topic']
        self._type = type_
        super(ForumToolsIDField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from .forms import ForumIDField, TopicIDField
        if self._type == 'forum':
            form_class = ForumIDField
        elif self._type == 'topic':
            form_class = TopicIDField
        defaults = {'form_class': form_class}
        defaults.update(kwargs)
        return super(ForumToolsIDField, self).formfield(**defaults)

    def contribute_to_class(self, cls, name):
        """ Make an accessor for the ID field. """
        super(ForumToolsIDField, self).contribute_to_class(cls, name)
        setattr(cls, name, ForumToolsDescriptor(self))

    def get_attname(self):
        return "{0}_id".format(self.name)

    def get_attname_column(self):
        attname, column = super(ForumToolsIDField, self).get_attname_column()
        return attname, column


class ForumToolsDescriptor(object):

    def __init__(self, related):
        self.related = related
        self.type = related._type
        self.cache_name = related.get_cache_name() # TODO: strip of the ID

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            rel_obj = getattr(instance, self.cache_name)
        except AttributeError:
            pk = getattr(instance, self.related.attname)
            rel_obj = self.get_object(pk)
            setattr(instance, self.cache_name, rel_obj)
        return rel_obj

    def __set__(self, instance, value):
        if value is None and self.related.null == False:
            value = 0
        elif value is None:
            setattr(instance, self.related.attname, None)
            setattr(instance, self.cache_name, None)
        elif value is not None:
            if isinstance(value, int):
                setattr(instance, self.related.attname, value)
            else:
                self.check_type(instance, value)
                setattr(instance, self.cache_name, value)
                setattr(instance, self.related.attname, value.pk)

    def get_object(self, pk):
        from brouwers.forum_tools.models import Forum, Topic
        if self.type == 'topic':
            model = Topic
        elif self.type == 'forum':
            model = Forum
        else:
            raise ValueError('Unknown type: %s' % self.type)

        if not pk:
            return None

        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return None

    def check_type(self, instance, value):
        from brouwers.forum_tools.models import Forum, Topic
        if self.type == 'topic' and not isinstance(value, Topic):
            raise ValueError('Cannot assign "%r": "%s.%s" must be a "%s" instance.' %
                                (value, instance._meta.object_name,
                                    self.related.name, Topic._meta.object_name))
        elif self.type == 'forum' and not isinstance(value, Forum):
            raise ValueError('Cannot assign "%r": "%s.%s" must be a "%s" instance.' %
                                (value, instance._meta.object_name,
                                    self.related.name, Forum._meta.object_name))
        elif self.type not in ['topic', 'forum']:
            raise ValueError('Unknown type: %s' % self.type)




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
