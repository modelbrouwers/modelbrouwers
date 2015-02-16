from django.test import TestCase

from .factory_models import UserFactory
from ..forms import AdminUserCreationForm


class AuthFormTests(TestCase):

    def setUp(self):
        super(AuthFormTests, self).setUp()
        self.user = UserFactory.create()
