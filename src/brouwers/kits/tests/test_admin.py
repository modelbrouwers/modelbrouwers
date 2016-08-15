from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory
from ..models import ModelKit
from .factories import BrandFactory, ScaleFactory, ModelKitFactory


class AdminTests(WebTest):

    def setUp(self):
        self.superuser = UserFactory.create(is_staff=True, is_superuser=True)

    def test_merge_duplicate_brands(self):
        """
        Unit test the admin action to mark duplicate brands.
        """
        url = reverse('admin:kits_brand_changelist')
        brands = BrandFactory.create_batch(10)
        for brand in brands:
            ModelKitFactory.create(brand=brand)

        index_range = range(1, 4)  # 2nd, 3rd, 4th entry
        brand_list = self.app.get(url, user=self.superuser)
        form = brand_list.forms['changelist-form']

        form['action'].select('merge_duplicates')
        for index in index_range:
            field = form.get('_selected_action', index=index)
            field.checked = True

        intermediate = form.submit()
        form = intermediate.forms[1]

        expected_brands = [repr(brand) for i, brand in enumerate(brands) if i in index_range]
        self.assertQuerysetEqual(intermediate.context['queryset'], expected_brands)
        django_form = intermediate.context['form']
        queryset = django_form.fields['target'].queryset
        expected_targets = [repr(brand) for i, brand in enumerate(brands) if i not in index_range]
        self.assertQuerysetEqual(queryset, expected_targets)

        # select a target
        form['target'].select(brands[8].pk)
        form.submit().follow()

        kits = ModelKit.objects.filter(brand=brands[8])
        self.assertEqual(kits.count(), 4)
        self.assertEqual(ModelKit.objects.values('brand').distinct().count(), 7)
        self.assertEqual(ModelKit.objects.count(), 10)
