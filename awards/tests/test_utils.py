from datetime import date

from django.test import SimpleTestCase

from freezegun import freeze_time

from ..utils import voting_enabled


class UtilsTest(SimpleTestCase):

    def test_voting_enabled(self):
        with freeze_time("2014-01-01"):
            self.assertTrue(voting_enabled())
            self.assertFalse(voting_enabled(year=2013))
            self.assertFalse(voting_enabled(year=2015))

        with freeze_time("2014-01-30"):
            self.assertFalse(voting_enabled())
            self.assertTrue(voting_enabled(date(2014, 1, 5)))
            self.assertFalse(voting_enabled(date(2013, 12, 31)))
