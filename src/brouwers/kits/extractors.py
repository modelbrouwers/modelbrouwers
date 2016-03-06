from sniplates.templatetags.sniplates import FieldExtractor


class ModelKitExtractor(FieldExtractor):

    @property
    def selected_kits(self):
        queryset = self.form_field.field.queryset
        if len(self.raw_value):
            return queryset.filter(pk__in=self.raw_value)
        return queryset.none()
