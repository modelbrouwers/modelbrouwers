from django.test import TestCase

from ..models import Competition
from .factories import CompetitionFactory


class CurrentCompetitionTests(TestCase):
    def test_only_one_current_competition(self):
        """Test that at a given time, only one competition is marked as 'current'"""
        competition1 = CompetitionFactory(is_current=False)
        competition2 = CompetitionFactory(is_current=True)

        qs = Competition.objects.filter(is_current=True)
        self.assertEqual(qs.count(), 1)

        competition1.is_current = True
        competition1.save()

        self.assertEqual(qs.count(), 1)

        competition1 = Competition.objects.get(pk=competition1.pk)
        self.assertTrue(competition1.is_current)
        competition2 = Competition.objects.get(pk=competition2.pk)
        self.assertFalse(competition2.is_current)
