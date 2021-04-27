from django.conf import settings
from django.test.runner import DiscoverRunner


class TestDiscoverRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        settings.TESTING = True
        super().setup_test_environment(**kwargs)
