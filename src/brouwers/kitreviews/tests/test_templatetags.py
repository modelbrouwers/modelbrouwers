from __future__ import absolute_import, unicode_literals

from django.template import engines
from django.test import SimpleTestCase


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

    def test_rating_css_class(self):
        tpl = "{% load kitreviews %}{{ rating|rating_class }}"
        template = self._load_template(tpl)

        rendered = template.render({'rating': '100'})
        self.assertHTMLEqual(rendered, 'success')

        rendered = template.render({'rating': 79})
        self.assertHTMLEqual(rendered, 'info')

        rendered = template.render({'rating': '49'})
        self.assertHTMLEqual(rendered, 'warning')

        rendered = template.render({'rating': -1})
        self.assertHTMLEqual(rendered, 'danger')

        rendered = template.render({'rating': 19})
        self.assertHTMLEqual(rendered, 'danger')

        rendered = template.render({'rating': 'abcd'})
        self.assertHTMLEqual(rendered, '')
