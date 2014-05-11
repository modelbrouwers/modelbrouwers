from datetime import date

from django.test import TestCase

from ..models import Nomination
from .factory_models import NominationFactory, CategoryFactory

# TODO: mock date.today
# TODO: mock voting_enabled

class NominationManagerTests(TestCase):
    def setUp(self):
        # set a fixed nomination date for the sake of clarity
        self.nomination_date = date(2013, 10, 1)


    def test_winners_returned(self):
        """ Test that only the winners in categories are returned """
        # create two categories
        cat1 = CategoryFactory()
        cat2 = CategoryFactory()


        # create some projects in each category
        nom1 = NominationFactory(category=cat1, votes=1, nomination_date=self.nomination_date)
        nom2 = NominationFactory(category=cat1, votes=10, nomination_date=self.nomination_date)

        nom3 = NominationFactory(category=cat2, votes=10, nomination_date=self.nomination_date)
        nom4 = NominationFactory(category=cat2, votes=20, nomination_date=self.nomination_date)

        winners = Nomination.objects.winners(year=self.nomination_date.year)

        self.assertEqual(len(winners), 2)
        self.assertIn(nom2, winners)
        self.assertIn(nom4, winners)
        self.assertNotIn(nom1, winners)
        self.assertNotIn(nom3, winners)

    def test_winners_same_score(self):
        """ Test that winners with the same score are both included """
        category = CategoryFactory()

        nom1 = NominationFactory(category=category, votes=1, nomination_date=self.nomination_date)
        nom2 = NominationFactory(category=category, votes=10, nomination_date=self.nomination_date)
        nom3 = NominationFactory(category=category, votes=10, nomination_date=self.nomination_date)

        winners = Nomination.objects.winners(year=self.nomination_date.year)
        self.assertEqual(len(winners), 2)
        self.assertIn(nom2, winners)
        self.assertIn(nom3, winners)
        self.assertNotIn(nom1, winners)

    # TODO: test default year, voting_enabled False/True
