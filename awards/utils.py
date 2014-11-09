from datetime import date

from django.conf import settings


def voting_enabled(test_date=None, year=None):
    """
    Test if voting is possible for `test_date` or the year.

    :param year: Integer specifying if voting is active in this year. E.g. 2014
                 means testing if the 2013 nominations are being voted.
    """
    assert None in [test_date, year]  # only one of both options is possible
    test_date = test_date or date.today()
    this_year = date.today().year

    if year and year != this_year:  # the passed in year is the current year
        return False

    start = date(this_year, 1, 1)
    end = date(this_year, settings.VOTE_END_MONTH, settings.VOTE_END_DAY)
    if start <= test_date <= end:
        return True
    return False
