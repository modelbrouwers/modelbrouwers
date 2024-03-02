from datetime import date, timedelta

from django.test import TestCase

from brouwers.users.tests.factories import UserFactory

from ..models import GroupbuildDurations, GroupbuildStatuses
from .factories import GroupBuildFactory


class GroupbuildTests(TestCase):
    def test_calendar_dimensions(self):
        oct_1st = date(2013, 10, 1)
        jan_1st = date(2014, 1, 1)
        feb_15th = date(2014, 2, 15)
        april_1st = date(2014, 4, 1)
        may_15th = date(2014, 5, 15)
        jul_1st = date(2014, 7, 1)

        sept_1st = date(2014, 9, 1)
        oct_1st2 = date(2014, 10, 1)
        jan_1st2 = date(2015, 1, 1)
        march_1st = date(2015, 3, 1)
        jul_1st2 = date(2015, 7, 1)

        start = jan_1st
        end = jul_1st

        # start dates collide, end is halfway
        build1 = GroupBuildFactory.create(start=jan_1st, end=april_1st)
        build1.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build1.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 50.5, delta=0.1)
        self.assertAlmostEqual(dimensions["offset"], 0.0, delta=0.05)

        # start is half before, end is halfway
        build2 = GroupBuildFactory.create(start=oct_1st, end=april_1st)
        build2.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build2.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 50.5, delta=0.5)
        self.assertAlmostEqual(dimensions["offset"], 0.0, delta=0.05)

        # start is halfway, end is end date
        build3 = GroupBuildFactory.create(start=april_1st, end=oct_1st2)
        build3.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build3.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 49.75, delta=0.5)
        self.assertAlmostEqual(dimensions["offset"], 50.5, delta=0.5)

        # both end and start in the interval
        build4 = GroupBuildFactory.create(start=feb_15th, end=may_15th)
        build4.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build4.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 50, delta=0.5)
        self.assertAlmostEqual(dimensions["offset"], 25, delta=0.6)

        # interval end in the middle of the build
        build5 = GroupBuildFactory.create(start=april_1st, end=oct_1st2)
        build5.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build5.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 50.0, delta=0.6)
        self.assertAlmostEqual(dimensions["offset"], 50.5, delta=0.5)

        # build longer than interval
        build6 = GroupBuildFactory.create(start=oct_1st, end=oct_1st2)
        build6.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build6.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 100.0, places=2)
        self.assertAlmostEqual(dimensions["offset"], 0.0, places=2)

        # test stuff in the next year
        build7 = GroupBuildFactory.create(start=jan_1st2, end=jul_1st2)
        build7.set_calendar_dimensions(date(2014, 9, 1), date(2015, 3, 1), num_months=6)
        dimensions = build7.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 33.33, places=2)
        self.assertAlmostEqual(dimensions["offset"], 66.67, places=2)

        build8 = GroupBuildFactory.create(start=sept_1st, end=march_1st, theme="foo")
        build8.set_calendar_dimensions(
            date(2014, 12, 1), date(2015, 5, 30), num_months=6
        )
        dimensions = build8.calendar_dimensions
        self.assertAlmostEqual(dimensions["width"], 50.5, delta=0.5)
        self.assertAlmostEqual(dimensions["offset"], 0.0, places=2)

    def test_is_ongoing(self):
        """Test that the model correctly returns the 'ongoing' status"""
        start1 = date.today() - timedelta(hours=24)
        end1 = date.today() + timedelta(hours=24)
        gb1 = GroupBuildFactory.create(start=start1, end=end1)
        self.assertTrue(gb1.is_ongoing)

        end2 = date.today() - timedelta(hours=24)
        gb2 = GroupBuildFactory.create(end=end2)
        self.assertFalse(gb2.is_ongoing)

        start3 = date.today() + timedelta(hours=24)
        gb3 = GroupBuildFactory.create(start=start3)
        self.assertFalse(gb3.is_ongoing)

        gb4 = GroupBuildFactory.create(start=None, end=None)
        self.assertFalse(gb4.is_ongoing)

    def test_is_open(self):
        gb1 = GroupBuildFactory.create(status=GroupbuildStatuses.denied)
        self.assertFalse(gb1.is_open)

        gb2 = GroupBuildFactory(end=date.today() - timedelta(hours=24))
        self.assertFalse(gb2.is_open)

        for status, label in GroupbuildStatuses.choices:
            if status != GroupbuildStatuses.denied:
                gb = GroupBuildFactory.create(status=status)
                self.assertTrue(gb.is_open)

    def test_progress(self):
        start1 = date.today() - timedelta(hours=24)
        end1 = date.today() + timedelta(hours=24)

        gb1 = GroupBuildFactory.create(start=start1, end=end1)
        self.assertAlmostEqual(gb1.progress, 0.5, delta=0.01)

        # no start or end date
        gb2 = GroupBuildFactory.create(start=None)
        self.assertEqual(gb2.progress, 0)

        gb3 = GroupBuildFactory.create(end=None)
        self.assertEqual(gb3.progress, 0)

        # ratio's
        start4 = date.today() - timedelta(hours=24 * 42)
        end4 = date.today() + timedelta(hours=24 * 21)
        gb4 = GroupBuildFactory.create(start=start4, end=end4)
        progress = 2.0 / 3
        self.assertAlmostEqual(gb4.progress, progress, delta=0.1)

    def test_is_submittable(self):
        """Test if the groupbuild is submittable"""
        build1 = GroupBuildFactory.create(start=None)
        self.assertFalse(build1.is_submittable)

        build2 = GroupBuildFactory.create(end=None)
        self.assertFalse(build2.is_submittable)

        for status in GroupbuildStatuses.values:
            build = GroupBuildFactory.create(
                start=date(2014, 10, 1),
                duration=GroupbuildDurations.one_month,
                status=status,
            )
            if status == GroupbuildStatuses.concept:
                self.assertTrue(build.is_submittable)
            else:
                self.assertFalse(build.is_submittable)

    def test_submitter_is_admin(self):
        """
        Test that the applicant is an admin of the build.
        """
        user = UserFactory.create()
        gb = GroupBuildFactory.create(applicant=user)
        self.assertQuerySetEqual(
            gb.admins.all(), [repr(user)], ordered=False, transform=repr
        )

        gb.save()  # trigger signal
        self.assertEqual(gb.admins.count(), 1)

        # test that existing groupbuilds aren't forced
        gb = gb.__class__.objects.get(pk=gb.pk)
        gb.admins.remove(gb.applicant)
        self.assertQuerySetEqual(gb.admins.all(), [], ordered=False, transform=repr)
