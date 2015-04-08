from django.conf import settings
from django.test.runner import DiscoverRunner


class TestDiscoverRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        settings.TESTING = True
        super(TestDiscoverRunner, self).setup_test_environment(**kwargs)
