import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..models import QuestionAnswer, RegistrationQuestion, UserProfile


class QuestionAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionAnswer

    answer = "answer"


class RegistrationQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistrationQuestion

    question = factory.Sequence(lambda n: "Question {n}".format(n=n))
    in_use = True

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            for answer in extracted:
                self.answers.add(answer)
        else:
            self.answers.add(QuestionAnswerFactory(**kwargs))


class UserProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    street = factory.Faker('name')
    number = factory.Faker('name', length=10)
    postal = factory.Faker('postcode')
    city = factory.Faker('city')
    country = 'N'

    class Meta:
        model = UserProfile
