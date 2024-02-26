import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..models import UserProfile


class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    street = factory.Faker("name")
    number = factory.Faker("name", length=10)
    postal = factory.Faker("postcode")
    city = factory.Faker("city")
    country = "N"

    class Meta:
        model = UserProfile
