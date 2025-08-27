from textwrap import dedent

from django.template import TemplateSyntaxError, engines
from django.test import TestCase

from .factories import CategoryFactory


class RecordCategoryPathTests(TestCase):
    def _load_template(self, tpl):
        return engines["django"].from_string(tpl)

    def test_invalid_args(self):
        invalid = (
            "{% record_category_path %}",
            "{% record_category_path item %}",
            "{% record_category_path item info %}",
            "{% record_category_path item info category_path %}",
            "{% record_category_path item info foo category_path %}",
        )
        for tpl in invalid:
            with self.subTest(template=tpl):
                full_tpl = "{% load shop %}" + tpl
                with self.assertRaises(TemplateSyntaxError):
                    self._load_template(full_tpl)

    def test_process_tree_correctly(self):
        root = CategoryFactory.create(slug="root")
        child1 = CategoryFactory.create(slug="child-1", parent=root)
        CategoryFactory.create(slug="child-1-1", parent=child1)
        child12 = CategoryFactory.create(slug="child-1-2", parent=child1)
        CategoryFactory.create(slug="child-1-2-1", parent=child12)
        CategoryFactory.create(slug="child-2", parent=root)
        tpl = dedent(
            """
            {% load shop %}
            {% category_tree 4 as categories %}
            {% for item, info in categories %}
            {% record_category_path item info as category_path %}{{ category_path }}{% endfor %}
        """
        ).strip()
        template = self._load_template(tpl)

        output = template.render({}).strip()

        expected = dedent(
            """
            root
            root/child-1
            root/child-1/child-1-1
            root/child-1/child-1-2
            root/child-1/child-1-2/child-1-2-1
            root/child-2
            """
        ).strip()
        self.assertEqual(output, expected)
