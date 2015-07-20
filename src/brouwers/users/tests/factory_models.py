import warnings

from .factories import *

warnings.warn('Import from users.tests.factories, the factory_models '
              'module will be removed', PendingDeprecationWarning)
