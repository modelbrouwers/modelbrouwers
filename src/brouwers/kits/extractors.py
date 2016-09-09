from django.utils.functional import cached_property

from sniplates.templatetags.sniplates import FieldExtractor


class ModelKitExtractor(FieldExtractor):

    @property
    def selected_kits(self):
        queryset = self.form_field.field.queryset
        if self.raw_value:
            return queryset.filter(pk=self.raw_value)
        return queryset.none()

    @cached_property
    def selected_brand(self):
        initial = self.form_field.form.initial.get(self.form_field.name)
        if initial:
            return str(initial.brand_id)
        return ''

    @cached_property
    def selected_scale(self):
        initial = self.form_field.form.initial.get(self.form_field.name)
        if initial:
            return str(initial.scale_id)
        return ''

    @cached_property
    def selected_name(self):
        initial = self.form_field.form.initial.get(self.form_field.name)
        if initial:
            return initial.name
        return ''


class MultiModelKitExtractor(FieldExtractor):

    @property
    def selected_kits(self):
        queryset = self.form_field.field.queryset
        if len(self.raw_value):
            return queryset.filter(pk__in=self.raw_value)
        return queryset.none()
