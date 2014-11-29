import warnings

from awards.utils import voting_enabled as _voting_enabled


def voting_enabled(test_date=None, year=None):
	warnings.warn(
        "Don't use this anymore - it's moved to awards.utils",
        DeprecationWarning
    )
	return _voting_enabled(test_date=test_date, year=year)
