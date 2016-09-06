from django.test import TestCase

from ..models import GroupBuild, GroupbuildStatuses
from .factories import GroupBuildFactory


class ManagerTests(TestCase):

    def setUp(self):
        # create some groupbuilds
        self.gb_concept = GroupBuildFactory(status=GroupbuildStatuses.concept)
        self.gb_submitted = GroupBuildFactory(status=GroupbuildStatuses.submitted)
        self.gb_accepted = GroupBuildFactory(status=GroupbuildStatuses.accepted)
        self.gb_denied = GroupBuildFactory(status=GroupbuildStatuses.denied)
        self.gb_extended = GroupBuildFactory(status=GroupbuildStatuses.extended)

    def test_public_manager(self):
        public_gbs = GroupBuild.public.all()
        for gb in [self.gb_concept, self.gb_submitted, self.gb_accepted, self.gb_extended]:
            self.assertIn(gb, public_gbs)
