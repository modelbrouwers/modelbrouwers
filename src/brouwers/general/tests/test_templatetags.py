import unittest

from django.template import Context, Template, TemplateSyntaxError, engines
from django.test import SimpleTestCase


class BlockVerbatimTestCase(unittest.TestCase):
    """
    Testcase testing the block_verbatim template tag.

    block_verbatim parses other template tags while leaving {{foo}} structures
    untouched. {% block %} inside block_verbatim DOES render context variables.
    """

    def test_render(self):
        """ Test block_verbatim with block name in closing tag """
        t = Template(
            '{% load handlebars %}'  # load the tag library
            '{% block_verbatim test %}'
            '{{verbatim node}}'
            '{% endblock_verbatim test %}'
        )
        rendered = t.render(Context())

        self.assertEqual(rendered, u'{{verbatim node}}')

    def test_render_no_name_closing_tag(self):
        """ Test block_verbatim without block name in closing tag """
        t = Template(
            '{% load handlebars %}'  # load the tag library
            '{% block_verbatim test %}'
            '{{verbatim node}}'
            '{% endblock_verbatim %}'
        )
        rendered = t.render(Context())

        self.assertEqual(rendered, u'{{verbatim node}}')

    def test_block_in_block(self):
        t = Template(
            '{% load handlebars %}'  # load the tag library
            '{% block_verbatim test %}'
            '{{verbatim node}}'
            '{% block foo %}'
            '\nfoo'
            '{% endblock %}'
            '{% endblock_verbatim %}'
        )
        rendered = t.render(Context())

        self.assertEqual(rendered, u'{{verbatim node}}\nfoo')

    def test_block_in_block_with_context(self):
        t = Template(
            '{% load handlebars %}'  # load the tag library
            '{% block_verbatim test %}'
            '{{verbatim node}}'
            '{% block foo %}'
            '\n{{ foo }}'
            '{% endblock %}'
            '{% endblock_verbatim %}'
        )
        c = Context({'foo': 'bar'})
        rendered = t.render(c)

        self.assertEqual(rendered, u'{{verbatim node}}\nbar')

    def test_tag_not_loaded(self):
        def _create_template():
            Template(
                '{% block_verbatim test %}'
                '{{verbatim node}}'
                '{% endblock_verbatim %}'
            )

        self.assertRaises(TemplateSyntaxError, _create_template)


class KitReviewTagsTests(SimpleTestCase):
    def _load_template(self, tpl):
        return engines['django'].from_string(tpl)

    def test_review_rating(self):
        tpl = """
        {% load brouwers %}
        {% review_rating rating num_stars=num_stars %}
        """
        template = self._load_template(tpl)
        rendered = template.render({'rating': 80, 'num_stars': 5})
        self.assertHTMLEqual(
            rendered,
            '<i class="fa fa-star"></i>' * 4 +
            '<i class="fa fa-star-o"></i>'
        )

        rendered2 = template.render({'rating': 75, 'num_stars': 10})
        self.assertHTMLEqual(
            rendered2,
            '<i class="fa fa-star"></i>' * 7 +
            '<i class="fa fa-star-half-o"></i>' +
            '<i class="fa fa-star-o"></i>' * 2
        )

        rendered3 = template.render({'rating': 65, 'num_stars': 5})
        self.assertHTMLEqual(
            rendered3,
            '<i class="fa fa-star"></i>' * 3 +
            '<i class="fa fa-star-half-o"></i>' +
            '<i class="fa fa-star-o"></i>' * 1
        )
