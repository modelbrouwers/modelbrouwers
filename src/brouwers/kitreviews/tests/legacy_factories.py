from datetime import datetime

import factory
import factory.fuzzy


class CategorieFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'kitreviews.Categorie'

    naam = factory.Faker('sentence')


class FabrikantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'kitreviews.Fabrikant'

    naam = factory.Faker('sentence')


class KitFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'kitreviews.Kit'

    categorie = factory.SubFactory(CategorieFactory)
    fabrikant = factory.SubFactory(FabrikantFactory)
    modelnaam = factory.Faker('word')
    moeilijkheid = factory.fuzzy.FuzzyInteger(1, 5)
    datum = factory.fuzzy.FuzzyDateTime(datetime(2005, 1, 1))


class ReviewerFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'kitreviews.Reviewer'

    naam = factory.Faker('full_name')
    emailadres = factory.Faker('email')


class ReviewFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'kitreviews.Review'

    commentaar = factory.Faker('text')
    indruk = factory.fuzzy.FuzzyInteger(1, 5)
    kit = factory.SubFactory(KitFactory)
    reviewer = factory.SubFactory(ReviewerFactory)
    datum = factory.fuzzy.FuzzyDateTime(datetime(2005, 1, 1))
