from datetime import date

from django.test import TestCase

from .factories import GroupBuildFactory


class GroupbuildTests(TestCase):

    def test_calendar_dimensions(self):
        oct_1st = date(2013, 10, 1)
        jan_1st = date(2014, 1, 1)
        feb_15th = date(2014, 2, 15)
        april_1st = date(2014, 4, 1)
        may_15th = date(2014, 5, 15)
        jul_1st = date(2014, 7, 1)
        oct_1st2 = date(2014, 10, 1)

        start = jan_1st
        end = jul_1st

        # start dates collide, end is halfway
        build1 = GroupBuildFactory.create(start=jan_1st, end=april_1st)
        build1.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build1.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 50.5, delta=0.1)
        self.assertAlmostEqual(dimensions['offset'], 0.0, delta=0.05)

        # start is half before, end is halfway
        build2 = GroupBuildFactory.create(start=oct_1st, end=april_1st)
        build2.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build2.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 33.3, delta=0.5)
        self.assertAlmostEqual(dimensions['offset'], 0.0, delta=0.05)

        # start is halfway, end is end date
        build3 = GroupBuildFactory.create(start=april_1st, end=oct_1st2)
        build3.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build3.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 50, delta=0.5)
        self.assertAlmostEqual(dimensions['offset'], 50, delta=0.5)

        # both end and start in the interval
        build4 = GroupBuildFactory.create(start=feb_15th, end=may_15th)
        build4.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build4.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 50, delta=0.05)
        self.assertAlmostEqual(dimensions['offset'], 8.93, delta=0.1)

        # interval end in the middle of the build
        build5 = GroupBuildFactory.create(start=april_1st, end=oct_1st2)
        build5.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build5.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 33.3, delta=0.5)
        self.assertAlmostEqual(dimensions['offset'], 50.0, delta=0.5)

        # build longer than interval
        build6 = GroupBuildFactory.create(start=oct_1st, end=oct_1st2)
        build6.set_calendar_dimensions(start, end, num_months=6)
        dimensions = build6.calendar_dimensions
        self.assertAlmostEqual(dimensions['width'], 100.0, places=2)
        self.assertAlmostEqual(dimensions['offset'], 0.0, places=2)

