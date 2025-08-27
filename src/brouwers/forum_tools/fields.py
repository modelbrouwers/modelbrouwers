from django.db.models.fields import PositiveIntegerField
from django.db.models.fields.mixins import FieldCacheMixin


class ForumToolsIDField(FieldCacheMixin, PositiveIntegerField):
    def __init__(self, *args, **kwargs):
        type_ = kwargs.pop("type")
        assert type_ in ["forum", "topic"]
        self._type = type_
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["type"] = self._type
        return (name, path, args, kwargs)

    def formfield(self, **kwargs):
        from .forms import ForumIDField, TopicIDField

        if self._type == "forum":
            form_class = ForumIDField
        elif self._type == "topic":
            form_class = TopicIDField
        defaults = {"form_class": form_class}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def contribute_to_class(self, cls, name):
        """Make an accessor for the ID field."""
        super().contribute_to_class(cls, name)
        setattr(cls, name, ForumToolsDescriptor(self))

    def get_attname(self):
        return f"{self.name}_id"

    def get_attname_column(self):
        attname, column = super().get_attname_column()
        return attname, column

    def get_cache_name(self):
        return self.name


class ForumToolsDescriptor:
    def __init__(self, field_with_rel):
        self.field = field_with_rel
        self.type = field_with_rel._type

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            rel_obj = self.field.get_cached_value(instance)
        except KeyError:
            pk = getattr(instance, self.field.attname)
            rel_obj = self.get_object(pk)
            self.field.set_cached_value(instance, rel_obj)
        return rel_obj

    def __set__(self, instance, value):
        if value is None and self.field.null is False:
            value = 0
        elif value is None:
            setattr(instance, self.field.attname, None)
            self.field.set_cached_value(instance, None)
        elif value is not None:
            if isinstance(value, int):
                setattr(instance, self.field.attname, value)
            else:
                self.check_type(instance, value)
                self.field.set_cached_value(instance, value)
                setattr(instance, self.field.attname, value.pk)

    def get_object(self, pk):
        from brouwers.forum_tools.models import Forum, Topic

        if self.type == "topic":
            model = Topic
        elif self.type == "forum":
            model = Forum
        else:
            raise ValueError(f"Unknown type: {self.type}")

        if not pk:
            return None

        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return None

    def check_type(self, instance, value):
        from brouwers.forum_tools.models import Forum, Topic

        if self.type == "topic" and not isinstance(value, Topic):
            raise ValueError(
                f'Cannot assign "{value!r}": "{instance._meta.object_name}.{self.field.name}" must be a "{Topic._meta.object_name}" instance.'
            )
        elif self.type == "forum" and not isinstance(value, Forum):
            raise ValueError(
                f'Cannot assign "{value!r}": "{instance._meta.object_name}.{self.field.name}" must be a "{Forum._meta.object_name}" instance.'
            )
        elif self.type not in ["topic", "forum"]:
            raise ValueError(f"Unknown type: {self.type}")
