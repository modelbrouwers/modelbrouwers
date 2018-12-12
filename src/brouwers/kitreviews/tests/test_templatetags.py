from __future__ import absolute_import, unicode_literals

from django.template import engines
from django.test import SimpleTestCase


class KitReviewTagsTests(SimpleTestCase):

    def _load_template(self, tpl):
        return engines['django'].from_string(tpl)

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
