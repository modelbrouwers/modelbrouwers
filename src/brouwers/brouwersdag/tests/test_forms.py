from django.contrib.auth import \
    get_user_model  # otherwise we run intro troubles with the modelform
from django.urls import reverse

from django_webtest import WebTest

from brouwers.kits.tests.factories import BrandFactory
from brouwers.users.tests.factories import UserFactory

from ..forms import ShowCasedModelSignUpForm
from .factories import CompetitionFactory, ShowCasedModelFactory

User = get_user_model()


class CompetitionSignUpTests(WebTest):

    def setUp(self):
        self.competition = CompetitionFactory(max_num_models=1, is_current=True)
        self.brand = BrandFactory.create()
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
        competition = CompetitionFactory.create()

        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_limit_authenticated_user(self):
        """ Test that the limit per user is respected (user authenticated)"""
        user = UserFactory.create()

        # create one model belonging to self.competition
        ShowCasedModelFactory.create(owner=user, competition=self.competition, is_competitor=True)
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 1)

        # try to add a new one, add the user to the form data
        self.form_data['owner'] = user.pk
        form = ShowCasedModelSignUpForm(competition=self.competition, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('__all__'))

    def test_limit_anonymous(self):
        """ Test that the limit per user is respected (user not authenticated)"""
        # create one model belonging to self.competition
        ShowCasedModelFactory.create(competition=self.competition, is_competitor=True, email='test@testing.com')
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
        competition = CompetitionFactory.create(max_participants=0, max_num_models=5)
        ShowCasedModelFactory.create(competition=competition, is_competitor=True, email='test@testing.com')

        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_participant_limit(self):
        """ Test that the absolute participant limit is respected """
        competition = CompetitionFactory.create(max_participants=1)
        ShowCasedModelFactory.create(competition=competition, is_competitor=True, email='test@testing.com')

        self.assertEqual(competition.showcasedmodel_set.all().count(), 1)
        form = ShowCasedModelSignUpForm(competition=competition, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIsNotNone(form.errors.get('__all__'))

    def test_form_submit(self):
        """ Integration test: Test the url and submit data """
        url = reverse('brouwersdag:model-signup')

        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 0)

        signup = self.app.get(url)
        for key, value in self.form_data.items():
            signup.form[key] = value

        response = signup.form.submit()

        self.assertRedirects(response, url)
        self.assertEqual(self.competition.showcasedmodel_set.all().count(), 1)
