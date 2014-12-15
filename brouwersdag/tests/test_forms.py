from django.test import TestCase
from django.contrib.auth import get_user_model # otherwise we run intro troubles with the modelform
User = get_user_model()

from kitreviews.tests.factories import BrandFactory
from users.tests.factory_models import UserFactory

from .factories import CompetitionFactory, ShowCasedModelFactory
from ..forms import ShowCasedModelSignUpForm

from unittest import skip


class CompetitionSignUpTests    (TestCase):
    def setUp(self):
        self.competition = CompetitionFactory(max_num_models=1, is_current=True)
        self.brand = BrandFactory()
        self.form_data = {
            'owner_name': 'John Johnson',
            'brand': self.brand.pk,
            'name': 'My awesome model',
            'email': 'test@testing.com',
            'scale': 48,
            'is_competitor': True,
            'add_another': True,
        }

    def test_unlimited_competition(self):
        """ Test that the number of models per participant is unlimited """
        competition = CompetitionFactory()

        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_limit_authenticated_user(self):
        """ Test that the limit per user is respected (user authenticated)"""
        user = UserFactory()

        # create one model belonging to self.competition
        ShowCasedModelFactory(owner=user, competition=self.competition, is_competitor=True)
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 1)

        # try to add a new one, add the user to the form data
        self.form_data['owner'] = user.pk
        form = ShowCasedModelSignUpForm(competition=self.competition, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('__all__'))

    def test_limit_anonymous(self):
        """ Test that the limit per user is respected (user not authenticated)"""
        # create one model belonging to self.competition
        ShowCasedModelFactory(competition=self.competition, is_competitor=True, email='test@testing.com')
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 1)

        # try to add a new one, add the user to the form data
        form = ShowCasedModelSignUpForm(competition=self.competition, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('__all__'))

    def test_limit_allows_submit(self):
        """ Test that the limit is not too aggressive """
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 0)

        form = ShowCasedModelSignUpForm(competition=self.competition, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_limit_zero_is_infinite(self):
        """ Test that the limit '0' is not misinterpreted """
        competition = CompetitionFactory(max_participants=0, max_num_models=5)
        ShowCasedModelFactory(competition=competition, is_competitor=True, email='test@testing.com')

        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_participant_limit(self):
        """ Test that the absolute participant limit is respected """
        competition = CompetitionFactory(max_participants=1)
        ShowCasedModelFactory(competition=competition, is_competitor=True, email='test@testing.com')

        self.assertEqual(competition.showcasedmodel_set.all().count(), 1)
        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('__all__'))

    def test_form_submit(self):
        """ Integration test: Test the url and submit data """
        url = '/brouwersdag/sign-up/'

        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 0)
        response = self.client.post(url, self.form_data)
        self.assertRedirects(response, url)
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 1)
