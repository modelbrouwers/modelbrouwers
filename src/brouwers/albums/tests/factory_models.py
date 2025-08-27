import warnings

from .factories import *

warnings.warn(
    "Import from albums.tests.factories, the factory_models module will be removed",
    PendingDeprecationWarning,
)
