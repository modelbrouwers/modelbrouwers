import factory

from ..models import RegistrationQuestion, QuestionAnswer


class QuestionAnswerFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = QuestionAnswer

    answer = 'answer'


class RegistrationQuestionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = RegistrationQuestion

    question = factory.Sequence(lambda n: 'Question {n}'.format(n=n))
    in_use = True

    @factory.post_generation
    def answers(self, create, extracted, **kwargs):
        if extracted:
            # A list of groups were passed in, use them
            for answer in extracted:
                self.answers.add(answer)
        else:
            self.answers.add(QuestionAnswerFactory(**kwargs))
