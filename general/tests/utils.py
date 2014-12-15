import logging

from django.db.models.loading import get_models
from django.test.runner import DiscoverRunner


class UnmanagedTablesTestRunner(DiscoverRunner):
    """ Mixin that makes sure that unmanaged tables get created in tests. """
    def setup_test_environment(self, *args, **kwargs):
        self.unmanaged_models = [m for m in get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnmanagedTablesTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnmanagedTablesTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False


# turn of factory boy logging
logging.getLogger("factory").setLevel(logging.WARN)
