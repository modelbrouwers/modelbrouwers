# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import io

from django.test import TestCase
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from .factories import CategoryFactory


class CategoryImportExportTest(WebTest):

    def setUp(self):
        self.category = CategoryFactory.create()
        self.superuser = UserFactory.create(is_staff=True, is_superuser=True)

    def test_export(self):
        url = reverse('admin:shop_category_export')
        categories = self.app.get(url, user=self.superuser)
        form = categories.forms[1]
        form['file_format'].select('0')
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)
        export_fields = ['id', 'name', 'image', 'seo_keyword', 'enabled']

        self.assertEqual(headers, export_fields)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = CategoryFactory.create()

    def test_nesting(self):
        root = self.category.add_root(name='Root')
        self.assertEquals(root.name, 'Root')

        child1 = root.add_child(name='Child')
        child1.save()
        child2 = root.add_child(name='Child2')
        child2.save()

        self.assertEquals(len(root.get_children()), 2)

        child1.add_child()
        self.assertEquals(len(child1.get_children()), 1)
