from django.template import engines
from django.test import SimpleTestCase


class RatingTests(SimpleTestCase):
    def _load_template(self, tpl):
        return engines["django"].from_string(tpl)

    def test_review_rating(self):
        tpl = """
        {% load brouwers %}
        {% review_rating rating num_stars=num_stars %}
        """
        template = self._load_template(tpl)
        rendered = template.render({"rating": 80, "num_stars": 5})
        self.assertHTMLEqual(
            rendered, '<i class="fa fa-star"></i>' * 4 + '<i class="fa fa-star-o"></i>'
        )

        rendered2 = template.render({"rating": 75, "num_stars": 10})
        self.assertHTMLEqual(
            rendered2,
            '<i class="fa fa-star"></i>' * 7
            + '<i class="fa fa-star-half-o"></i>'
            + '<i class="fa fa-star-o"></i>' * 2,
        )

        rendered3 = template.render({"rating": 65, "num_stars": 5})
        self.assertHTMLEqual(
            rendered3,
            '<i class="fa fa-star"></i>' * 3
            + '<i class="fa fa-star-half-o"></i>'
            + '<i class="fa fa-star-o"></i>' * 1,
        )
